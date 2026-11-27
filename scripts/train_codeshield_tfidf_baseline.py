#!/usr/bin/env python3
"""Train a six-class TF-IDF-only baseline for CodeShield."""

import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
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


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "code" / "backend"
DATA = BACKEND / "data" / "processed"
MODEL_DIR = BACKEND / "codeshield_ml" / "models"

MODEL_PATH = MODEL_DIR / "codeshield_vulnerability_model_tfidf_baseline.joblib"
METRICS_PATH = MODEL_DIR / "tfidf_baseline_metrics.json"
REPORT_PATH = MODEL_DIR / "tfidf_baseline_classification_report.json"
CONFUSION_PATH = MODEL_DIR / "tfidf_baseline_confusion_matrix.csv"

LABELS = [
    "Command Injection",
    "Cross-Site Scripting",
    "Hardcoded Credentials",
    "Insecure File Handling",
    "SAFE",
    "SQL Injection",
]


def load_split(name):
    path = DATA / f"{name}.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing dataset split: {path}")

    frame = pd.read_csv(path)

    required = {"code", "label"}
    if not required.issubset(frame.columns):
        raise ValueError(f"{path} must contain {required}")

    frame = frame.dropna(subset=["code", "label"]).copy()
    frame["code"] = frame["code"].astype(str)
    frame["label"] = frame["label"].astype(str)

    unknown = sorted(set(frame["label"]) - set(LABELS))
    if unknown:
        raise ValueError(f"Unexpected labels in {name}: {unknown}")

    return frame


def make_pipeline():
    return Pipeline([
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
            "clf",
            CalibratedClassifierCV(
                estimator=LinearSVC(
                    C=1.0,
                    class_weight="balanced",
                    max_iter=20000,
                ),
                method="sigmoid",
                cv=3,
            ),
        ),
    ])


def main():
    train = load_split("train")
    validation = load_split("validation")
    test = load_split("test")

    print("\n========== DATASET DISTRIBUTION ==========")

    for name, frame in [
        ("Train", train),
        ("Validation", validation),
        ("Test", test),
    ]:
        print(f"\n{name}: {len(frame)} samples")
        print(frame["label"].value_counts().reindex(
            LABELS, fill_value=0
        ).to_string())

    X_train = train["code"].tolist()
    y_train = train["label"].tolist()

    X_val = validation["code"].tolist()
    y_val = validation["label"].tolist()

    # Train only on the training split.
    print("\n========== VALIDATION EVALUATION ==========")

    model = make_pipeline()
    model.fit(X_train, y_train)

    val_predictions = model.predict(X_val)

    val_metrics = {
        "accuracy": float(accuracy_score(y_val, val_predictions)),
        "macro_precision": float(precision_score(
            y_val, val_predictions, average="macro", zero_division=0
        )),
        "macro_recall": float(recall_score(
            y_val, val_predictions, average="macro", zero_division=0
        )),
        "macro_f1": float(f1_score(
            y_val, val_predictions, average="macro", zero_division=0
        )),
    }

    for key, value in val_metrics.items():
        print(f"{key}: {value:.4f}")

    # Refit on train + validation, just like the EST procedure.
    print("\nRetraining on train + validation...")

    combined = pd.concat([train, validation], ignore_index=True)

    final_model = make_pipeline()
    final_model.fit(
        combined["code"].tolist(),
        combined["label"].tolist(),
    )

    # Evaluate once on the held-out test set.
    X_test = test["code"].tolist()
    y_test = test["label"].tolist()

    predictions = final_model.predict(X_test)

    test_metrics = {
        "accuracy": float(accuracy_score(y_test, predictions)),
        "macro_precision": float(precision_score(
            y_test, predictions, average="macro", zero_division=0
        )),
        "macro_recall": float(recall_score(
            y_test, predictions, average="macro", zero_division=0
        )),
        "macro_f1": float(f1_score(
            y_test, predictions, average="macro", zero_division=0
        )),
    }

    report = classification_report(
        y_test,
        predictions,
        labels=LABELS,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(
        y_test,
        predictions,
        labels=LABELS,
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    artifact = {
        "model": final_model,
        "classes": LABELS,
        "model_type": "Calibrated Linear SVM",
        "feature_type": "word-level TF-IDF unigram + bigram only",
    }

    joblib.dump(artifact, MODEL_PATH)

    metrics = {
        "model": "TF-IDF-only baseline",
        "features": "TF-IDF unigram and bigram",
        "classifier": "Calibrated Linear SVM",
        "classifier_parameters": {
            "C": 1.0,
            "class_weight": "balanced",
            "max_iter": 20000,
            "calibration": "sigmoid",
            "cv": 3,
        },
        "split_counts": {
            "train": len(train),
            "validation": len(validation),
            "test": len(test),
            "final_training": len(combined),
        },
        "validation": val_metrics,
        "test": test_metrics,
        "limitations": (
            "Small dataset; not validated for production security decisions."
        ),
    }

    METRICS_PATH.write_text(
        json.dumps(metrics, indent=2) + "\n",
        encoding="utf-8",
    )

    REPORT_PATH.write_text(
        json.dumps(report, indent=2) + "\n",
        encoding="utf-8",
    )

    pd.DataFrame(
        matrix,
        index=LABELS,
        columns=LABELS,
    ).to_csv(CONFUSION_PATH)

    print("\n========== HELD-OUT TEST RESULTS ==========")
    for key, value in test_metrics.items():
        print(f"{key}: {value:.4f}")

    print("\n========== PER-CLASS REPORT ==========")
    print(classification_report(
        y_test,
        predictions,
        labels=LABELS,
        zero_division=0,
    ))

    print("\n========== CONFUSION MATRIX ==========")
    print(pd.DataFrame(
        matrix,
        index=LABELS,
        columns=LABELS,
    ))

    print("\n========== SAVED FILES ==========")
    print("Model:", MODEL_PATH)
    print("Metrics:", METRICS_PATH)
    print("Report:", REPORT_PATH)
    print("Confusion matrix:", CONFUSION_PATH)

    print("\nExisting EST and production models were NOT overwritten.")


if __name__ == "__main__":
    main()
