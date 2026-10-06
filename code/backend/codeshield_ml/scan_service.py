"""Combine deterministic static findings with ML vulnerability assessment."""

from typing import Any

from .model import assess_code
from .static_rules import run_static_rules


SEVERITY_SCORES = {
    "NONE": 0,
    "LOW": 3,
    "MEDIUM": 6,
    "HIGH": 9,
    "CRITICAL": 10,
}


def scan_code(code: str, model: Any | None = None) -> dict:
    """Run static rules and ML classification for a source-code submission."""
    if not isinstance(code, str) or not code.strip():
        return {
            "success": False,
            "message": "No code provided",
            "total_vulnerabilities": 0,
            "vulnerabilities": [],
            "overall_risk": 0,
            "ml_assessment": None,
            "source": "static",
        }

    findings = []

    # 1. Deterministic static analysis.
    for issue in run_static_rules(code):
        severity = str(issue.get("severity", "LOW")).upper()

        findings.append({
            **issue,
            "confidence": issue.get("confidence", 0) / 100,
            "risk_score": SEVERITY_SCORES.get(severity, 3),
            "detection_method": "static",
        })

    # 2. ML classification.
    assessment = assess_code(code, model=model)

    # 3. Add the ML result to the unified findings list only when the model
    # predicts an actual vulnerability. SAFE is still returned in
    # ml_assessment, but should not inflate vulnerability counts.
    if assessment is not None and assessment.get("is_vulnerable"):
        findings.append({
            "type": assessment["vulnerability_type"],
            "severity": assessment["severity"],
            "confidence": assessment["confidence"],
            "risk_score": assessment["risk_score"],
            "cwe": assessment.get("cwe"),
            "detection_method": "ml",
        })

    highest_static_score = max(
        (finding["risk_score"] for finding in findings),
        default=0,
    )

    ml_score = (
        assessment.get("risk_score", 0)
        if assessment is not None
        else 0
    )

    overall_risk = max(highest_static_score, ml_score)

    return {
        "success": True,
        "total_vulnerabilities": len(findings),
        "vulnerabilities": findings,
        "overall_risk": overall_risk,
        "ml_assessment": assessment,
        "source": "ml+static" if assessment is not None else "static",
    }
