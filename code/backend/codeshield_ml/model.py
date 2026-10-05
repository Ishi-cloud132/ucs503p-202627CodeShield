"""Load and run the optional vulnerability classification model."""

from pathlib import Path
from typing import Any

import joblib

MODEL_PATH = Path(__file__).resolve().parents[1] / "models" / "vulnerability_model.joblib"


def load_model() -> Any | None:
    """Return the trained pipeline when present, otherwise allow static-only scans."""
    if not MODEL_PATH.is_file():
        return None
    try:
        return joblib.load(MODEL_PATH)
    except (OSError, ValueError, EOFError):
        return None


def assess_code(code: str, model: Any | None = None) -> dict[str, Any] | None:
    """Return the model label and confidence, or None if no model is available."""
    classifier = model if model is not None else load_model()
    if classifier is None:
        return None

    probabilities = classifier.predict_proba([code])[0]
    class_index = int(probabilities.argmax())
    return {
        "label": str(classifier.classes_[class_index]),
        "confidence": float(probabilities[class_index]),
    }