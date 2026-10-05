#!/usr/bin/env python3
"""Train a small baseline classifier for CodeShield's optional ML assessment."""

import argparse
import csv
import json
from pathlib import Path

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "code/backend/models/vulnerability_model.joblib"
METRICS_PATH = ROOT / "code/backend/models/metrics.json"

BOOTSTRAP_SAMPLES = [
    ("query = 'SELECT * FROM users WHERE id=' + user_id", "vulnerable"),
    ("cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))", "safe"),
    ("os.system('ping ' + hostname)", "vulnerable"),
    ("subprocess.run(['ping', hostname], check=True)", "safe"),
    ("password = 'admin123'", "vulnerable"),
    ("password = os.environ.get('APP_PASSWORD')", "safe"),
    ("query = f\"SELECT * FROM accounts WHERE name='{name}'\"", "vulnerable"),
    ("cursor.execute('SELECT * FROM accounts WHERE name=?', (name,))", "safe"),
    ("subprocess.Popen(command, shell=True)", "vulnerable"),
    ("subprocess.run(['grep', pattern, filename], check=False)", "safe"),
    ("api_key = 'sk_test_example'", "vulnerable"),
    ("api_key = settings.API_KEY", "safe"),
    ("query = 'DELETE FROM records WHERE id=%s' % record_id", "vulnerable"),
    ("cursor.execute('DELETE FROM records WHERE id=%s', (record_id,))", "safe"),
    ("secret = 'local-development-secret'", "vulnerable"),
    ("secret = get_secret('application')", "safe"),
    ("os.system('rm ' + filename)", "vulnerable"),
    ("subprocess.run(['rm', '--', filename], check=True)", "safe"),
    ("render_template_string('<h1>' + username + '</h1>')", "vulnerable"),
    ("return render_template('profile.html', username=username)", "safe"),
]


def load_samples(data_path: Path | None) -> tuple[list[str], list[str], str]:
    if data_path is None:
        samples = BOOTSTRAP_SAMPLES
        source = "built-in bootstrap examples"
    else:
        with data_path.open(newline="", encoding="utf-8") as data_file:
            samples = [
                (row["code"], row["label"].strip().lower())
                for row in csv.DictReader(data_file)
            ]
        source = str(data_path)

    if len(samples) < 4 or {label for _, label in samples} != {"safe", "vulnerable"}:
        raise ValueError("Training data must contain at least four rows and both labels: safe, vulnerable")
    return [code for code, _ in samples], [label for _, label in samples], source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, help="CSV file with code,label columns")
    args = parser.parse_args()

    code_samples, labels, data_source = load_samples(args.data)
    train_code, test_code, train_labels, test_labels = train_test_split(
        code_samples,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )
    model = Pipeline([
        ("features", TfidfVectorizer(analyzer="char", ngram_range=(2, 5), min_df=1)),
        ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced")),
    ])
    model.fit(train_code, train_labels)
    predictions = model.predict(test_code)

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    metrics = {
        "status": "baseline",
        "training_data": data_source,
        "sample_count": len(code_samples),
        "train_count": len(train_code),
        "test_count": len(test_code),
        "accuracy": accuracy_score(test_labels, predictions),
        "classification_report": classification_report(
            test_labels, predictions, labels=["safe", "vulnerable"],
            output_dict=True, zero_division=0,
        ),
        "limitations": "Small baseline; not validated for production security decisions.",
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved metrics to {METRICS_PATH}")
    print(f"Holdout accuracy: {metrics['accuracy']:.3f}")


if __name__ == "__main__":
    main()