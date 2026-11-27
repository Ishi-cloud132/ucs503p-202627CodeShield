 
#!/usr/bin/env python3
"""Train and evaluate CodeShield's six-class TF-IDF + AST model."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd

from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


# ============================================================
# PATHS AND CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

BACKEND = ROOT / "code" / "backend"

sys.path.insert(0, str(BACKEND))

from codeshield_ml.features import ASTStructuralFeatures

DATA = BACKEND / "data" / "processed"

MODEL_DIR = BACKEND / "codeshield_ml" / "models"

MODEL_PATH = MODEL_DIR / "codeshield_vulnerability_model_est.joblib"

METRICS_PATH = MODEL_DIR / "est_model_metrics.json"

REPORT_PATH = MODEL_DIR / "est_classification_report.json"

CONFUSION_PATH = MODEL_DIR / "est_confusion_matrix.csv"


# ============================================================
# SIX CLASS LABELS
# ============================================================

LABELS = [
    "Command Injection",
    "Cross-Site Scripting",
    "Hardcoded Credentials",
    "Insecure File Handling",
    "SAFE",
    "SQL Injection",
]


SEVERITY_MAP = {
    "SAFE": "NONE",
    "Command Injection": "CRITICAL",
    "Cross-Site Scripting": "MEDIUM",
    "Hardcoded Credentials": "HIGH",
    "Insecure File Handling": "HIGH",
    "SQL Injection": "HIGH",
}


CWE_MAP = {
    "SAFE": None,
    "Command Injection": "CWE-78",
    "Cross-Site Scripting": "CWE-79",
    "Hardcoded Credentials": "CWE-798",
    "Insecure File Handling": "CWE-22",
    "SQL Injection": "CWE-89",
}


# ============================================================
# LOAD DATASET SPLITS
# ============================================================

def load_split(name):

    path = DATA / f"{name}.csv"

    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run scripts/split_dataset.py first."
        )

    frame = pd.read_csv(path)

    required = {"code", "label"}

    if not required.issubset(frame.columns):
        raise ValueError(
            f"{path} must contain columns: {sorted(required)}"
        )

    frame = frame.dropna(subset=["code", "label"]).copy()

    frame["code"] = frame["code"].astype(str)
    frame["label"] = frame["label"].astype(str)

    unknown = sorted(set(frame["label"]) - set(LABELS))

    if unknown:
        raise ValueError(
            f"Unexpected labels in {name}: {unknown}"
        )

    return frame


# ============================================================
# FEATURE EXTRACTION + CLASSIFIER PIPELINE
# ============================================================

def make_pipeline(classifier):

    features = FeatureUnion([

        (
            "tfidf",

            TfidfVectorizer(
                max_features=50000,
                ngram_range=(1, 2),
                sublinear_tf=True,
                token_pattern=r"(?u)\b\w[\w$]*\b",
                min_df=1,
            ),
        ),

        (
            "ast",

            ASTStructuralFeatures(),
        ),

    ])

    return Pipeline([
        ("features", features),
        ("clf", classifier),
    ])


# ============================================================
# MAIN TRAINING FUNCTION
# ============================================================

def main():

    train = load_split("train")

    validation = load_split("validation")

    test = load_split("test")


    # --------------------------------------------------------
    # DISPLAY DATASET DISTRIBUTION
    # --------------------------------------------------------

    print("\n========== DATASET DISTRIBUTION ==========")

    for name, frame in [
        ("Train", train),
        ("Validation", validation),
        ("Test", test),
    ]:

        print(f"\n{name}: {len(frame)} samples")

        print(
            frame["label"]
            .value_counts()
            .reindex(LABELS, fill_value=0)
            .to_string()
        )


    X_train = train["code"].tolist()
    y_train = train["label"].tolist()

    X_val = validation["code"].tolist()
    y_val = validation["label"].tolist()


    # --------------------------------------------------------
    # THREE CLASSIFIERS TO COMPARE
    # --------------------------------------------------------

    candidates = {

        "Logistic Regression": LogisticRegression(
            max_iter=3000,
            class_weight="balanced",
            C=1.0,
        ),

        "Calibrated Linear SVM": CalibratedClassifierCV(
            estimator=LinearSVC(
                C=1.0,
                class_weight="balanced",
                max_iter=20000,
            ),
            method="sigmoid",
            cv=3,
        ),

        "Random Forest": RandomForestClassifier(
            n_estimators=300,
            class_weight="balanced_subsample",
            random_state=42,
            min_samples_leaf=1,
            n_jobs=-1,
        ),

    }


    # --------------------------------------------------------
    # TRAIN AND COMPARE MODELS USING VALIDATION DATA
    # --------------------------------------------------------

    results = []

    fitted = {}

    print("\n========== VALIDATION MODEL COMPARISON ==========")

    for name, classifier in candidates.items():

        print(f"\nTraining {name}...")

        pipeline = make_pipeline(classifier)

        pipeline.fit(X_train, y_train)

        predictions = pipeline.predict(X_val)

        macro_f1 = f1_score(
            y_val,
            predictions,
            average="macro",
            zero_division=0,
        )

        accuracy = accuracy_score(
            y_val,
            predictions,
        )

        macro_precision = precision_score(
            y_val,
            predictions,
            average="macro",
            zero_division=0,
        )

        macro_recall = recall_score(
            y_val,
            predictions,
            average="macro",
            zero_division=0,
        )

        results.append({

            "model": name,

            "validation_accuracy": float(accuracy),

            "validation_macro_precision": float(macro_precision),

            "validation_macro_recall": float(macro_recall),

            "validation_macro_f1": float(macro_f1),

        })

        fitted[name] = pipeline

        print(
            f"{name}: "
            f"Accuracy={accuracy:.4f}, "
            f"Macro-F1={macro_f1:.4f}, "
            f"Precision={macro_precision:.4f}, "
            f"Recall={macro_recall:.4f}"
        )


    # --------------------------------------------------------
    # SELECT BEST MODEL USING VALIDATION MACRO F1
    # --------------------------------------------------------

    best = max(
        results,
        key=lambda item: item["validation_macro_f1"],
    )

    best_name = best["model"]

    print("\n========================================")

    print("Selected model:", best_name)

    print(
        "Validation Macro-F1:",
        round(best["validation_macro_f1"], 4),
    )

    print("========================================")


    # --------------------------------------------------------
    # RETRAIN SELECTED MODEL ON TRAIN + VALIDATION
    # --------------------------------------------------------

    combined = pd.concat(
        [train, validation],
        ignore_index=True,
    )

    final_model = clone(fitted[best_name])

    print("\nRetraining selected model on train + validation...")

    final_model.fit(
        combined["code"].tolist(),
        combined["label"].tolist(),
    )


    # --------------------------------------------------------
    # FINAL TEST EVALUATION
    # --------------------------------------------------------

    X_test = test["code"].tolist()

    y_test = test["label"].tolist()

    test_predictions = final_model.predict(X_test)


    test_accuracy = accuracy_score(
        y_test,
        test_predictions,
    )

    test_macro_f1 = f1_score(
        y_test,
        test_predictions,
        average="macro",
        zero_division=0,
    )

    test_macro_precision = precision_score(
        y_test,
        test_predictions,
        average="macro",
        zero_division=0,
    )

    test_macro_recall = recall_score(
        y_test,
        test_predictions,
        average="macro",
        zero_division=0,
    )


    # --------------------------------------------------------
    # CLASSIFICATION REPORT
    # --------------------------------------------------------

    report = classification_report(
        y_test,
        test_predictions,
        labels=LABELS,
        output_dict=True,
        zero_division=0,
    )


    # --------------------------------------------------------
    # CONFUSION MATRIX
    # --------------------------------------------------------

    matrix = confusion_matrix(
        y_test,
        test_predictions,
        labels=LABELS,
    )


    # --------------------------------------------------------
    # SAVE MODEL AS A SEPARATE EST ARTIFACT
    # --------------------------------------------------------

    artifact = {

        "model": final_model,

        "classes": LABELS,

        "model_type": best_name,

        "feature_type": (
            "word-level TF-IDF unigram/bigram "
            "+ Python AST structural features"
        ),

        "best_validation_macro_f1": float(
            best["validation_macro_f1"]
        ),

        "target_column": "label",

        "text_column": "code",

        "excluded_columns": [
            "id",
            "cwe",
            "source",
        ],

        "severity_map": SEVERITY_MAP,

        "cwe_map": CWE_MAP,

        "language_scope": (
            "Python AST features; "
            "TF-IDF operates on source text"
        ),

    }


    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    joblib.dump(
        artifact,
        MODEL_PATH,
    )


    # --------------------------------------------------------
    # SAVE METRICS
    # --------------------------------------------------------

    metrics = {

        "status": "trained",

        "training_rows": int(len(train)),

        "validation_rows": int(len(validation)),

        "test_rows": int(len(test)),

        "final_fit_rows": int(len(combined)),

        "selected_model": best_name,

        "selection_metric": "validation_macro_f1",

        "validation_comparison": results,

        "test_metrics": {

            "accuracy": float(test_accuracy),

            "macro_precision": float(test_macro_precision),

            "macro_recall": float(test_macro_recall),

            "macro_f1": float(test_macro_f1),

        },

        "classes": LABELS,

        "feature_type": artifact["feature_type"],

        "note": (
            "Test metrics are from one held-out test evaluation "
            "after model selection on validation. Small class counts "
            "make per-class scores uncertain."
        ),

    }


    METRICS_PATH.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )


    REPORT_PATH.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )


    pd.DataFrame(
        matrix,
        index=LABELS,
        columns=LABELS,
    ).to_csv(
        CONFUSION_PATH,
        index=True,
    )


    # --------------------------------------------------------
    # DISPLAY FINAL RESULTS
    # --------------------------------------------------------

    print("\n========== HELD-OUT TEST RESULTS ==========")

    print(f"Accuracy:        {test_accuracy:.4f}")

    print(f"Macro Precision: {test_macro_precision:.4f}")

    print(f"Macro Recall:    {test_macro_recall:.4f}")

    print(f"Macro F1:        {test_macro_f1:.4f}")


    print("\n========== PER-CLASS REPORT ==========")

    print(
        classification_report(
            y_test,
            test_predictions,
            labels=LABELS,
            zero_division=0,
        )
    )


    print("\n========== CONFUSION MATRIX ==========")

    print(
        pd.DataFrame(
            matrix,
            index=LABELS,
            columns=LABELS,
        )
    )


    print("\n========== SAVED FILES ==========")

    print("Model:", MODEL_PATH)

    print("Metrics:", METRICS_PATH)

    print("Classification report:", REPORT_PATH)

    print("Confusion matrix:", CONFUSION_PATH)

    print("\nExisting production model was NOT overwritten.")


if __name__ == "__main__":
    main()
