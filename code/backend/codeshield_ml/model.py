"""CodeShield ML model integration.

Loads the calibrated vulnerability classifier trained from the CodeShield
dataset and exposes a small interface for the FastAPI scanning service.

Expected artifact:
    codeshield_ml/models/codeshield_vulnerability_model.joblib

The artifact contains:
    model, classes, best_C, text_column, excluded_columns,
    severity_map, cwe_map
"""

from pathlib import Path
from typing import Any

import joblib


MODEL_PATH = (
    Path(__file__).resolve().parent
    / "models"
    / "codeshield_vulnerability_model.joblib"
)


def load_model() -> dict[str, Any] | None:
    """Load the CodeShield model artifact, if it exists."""
    if not MODEL_PATH.is_file():
        return None

    try:
        artifact = joblib.load(MODEL_PATH)

        # The trained artifact is intentionally stored as a dictionary so
        # that the classifier, labels and risk metadata travel together.
        if isinstance(artifact, dict) and "model" in artifact:
            return artifact

        # Backwards compatibility if a raw sklearn estimator is supplied.
        return {
            "model": artifact,
            "classes": list(getattr(artifact, "classes_", [])),
            "severity_map": {},
            "cwe_map": {},
        }

    except (OSError, ValueError, EOFError, ImportError, AttributeError):
        return None


def assess_code(
    code: str,
    model: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Classify source code and return vulnerability/risk information."""
    if not isinstance(code, str) or not code.strip():
        return None

    artifact = model if model is not None else load_model()
    if artifact is None:
        return None

    classifier = artifact["model"]

    try:
        probabilities = classifier.predict_proba([code])[0]
        class_index = int(probabilities.argmax())
        label = str(classifier.classes_[class_index])
        confidence = float(probabilities[class_index])
    except (AttributeError, ValueError, TypeError):
        return None

    severity_map = artifact.get("severity_map", {})
    cwe_map = artifact.get("cwe_map", {})

    is_vulnerable = label != "SAFE"
    severity = severity_map.get(label, "UNKNOWN")
    if severity == "CRITICAL":
        severity = "HIGH"
    cwe = cwe_map.get(label)

    # Risk score is deliberately transparent. It is not claimed to be
    # learned by the ML model.
    severity_scores = {
        "NONE": 0,
        "LOW": 3,
        "MEDIUM": 6,
        "HIGH": 9,
        "UNKNOWN": 0,
    }

    return {
        "label": label,
        "vulnerability_type": None if not is_vulnerable else label,
        "is_vulnerable": is_vulnerable,
        "confidence": round(confidence, 4),
        "severity": severity,
        "cwe": cwe,
        "risk_score": severity_scores.get(severity, 0),
    }
