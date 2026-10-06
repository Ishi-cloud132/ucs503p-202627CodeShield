# CodeShield ML Backend Integration

Copy these four files into:

    code/backend/codeshield_ml/

Copy the trained artifact into:

    code/backend/codeshield_ml/models/codeshield_vulnerability_model.joblib

The existing `static_rules.py` does not need to be changed.

## Files

- `model.py`: loads the trained calibrated classifier and returns vulnerability type, confidence, severity, CWE and risk score.
- `scan_service.py`: combines static-rule findings and ML findings.
- `router.py`: exposes `POST /ml/scan`.
- `integration.py`: registers the router with the FastAPI application.

## Expected request

POST `/ml/scan`

```json
{
  "code": "user supplied source code"
}
```

## Example response

```json
{
  "success": true,
  "total_vulnerabilities": 1,
  "vulnerabilities": [
    {
      "type": "SQL Injection",
      "severity": "HIGH",
      "confidence": 0.94,
      "risk_score": 9,
      "cwe": "CWE-89",
      "detection_method": "ml"
    }
  ],
  "overall_risk": 9,
  "ml_assessment": {
    "label": "SQL Injection",
    "vulnerability_type": "SQL Injection",
    "is_vulnerable": true,
    "confidence": 0.94,
    "severity": "HIGH",
    "cwe": "CWE-89",
    "risk_score": 9
  },
  "source": "ml+static"
}
```

## Important

The ML model was trained using source code only. `cwe` and `source` were not model inputs.

Severity is a transparent category-to-risk mapping, not a learned severity prediction, because the supplied dataset does not contain an independent severity target.

## FastAPI registration

If `main.py` already calls `register_codeshield_ml(app)`, no additional route setup is required.

Otherwise:

```python
from codeshield_ml.integration import register_codeshield_ml

register_codeshield_ml(app)
```

Do not create a second `/ml` router if one is already registered.
