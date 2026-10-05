"""Combine deterministic findings with an optional ML risk assessment."""

from typing import Any

from .model import assess_code
from .static_rules import run_static_rules

SEVERITY_SCORES = {"HIGH": 9, "MEDIUM": 6, "LOW": 3}


def scan_code(code: str, model: Any | None = None) -> dict:
    findings = []
    for issue in run_static_rules(code):
        severity = issue.get("severity", "LOW")
        findings.append({
            **issue,
            "confidence": issue.get("confidence", 0) / 100,
            "risk_score": SEVERITY_SCORES.get(severity, 3),
        })

    assessment = assess_code(code, model=model)
    highest_static_score = max(
        (finding["risk_score"] for finding in findings), default=0
    )

    return {
        "success": True,
        "total_vulnerabilities": len(findings),
        "vulnerabilities": findings,
        "overall_risk": highest_static_score,
        "ml_assessment": assessment,
        "source": "ml+static" if assessment is not None else "static",
    }