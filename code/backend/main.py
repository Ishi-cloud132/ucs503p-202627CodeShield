from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from analyzers.static_analyzer import analyze_code
from services.risk_assessment import calculate_overall_risk


app = FastAPI(
    title="CodeShield API",
    description="Code vulnerability detection and risk assessment API",
    version="1.0.0"
)


# Allows the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "Welcome to CodeShield API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CodeShield Backend"
    }


@app.post("/scan")
def scan_code(data: dict):
    code = data.get("code", "")

    if not code.strip():
        return {
            "success": False,
            "message": "No code provided",
            "total_vulnerabilities": 0,
            "vulnerabilities": []
        }

    issues = analyze_code(code)

    vulnerabilities = []

    for issue in issues:
        severity = issue.get("severity", "LOW")

        risk_scores = {
            "HIGH": 9,
            "MEDIUM": 6,
            "LOW": 3
        }

        vulnerabilities.append({
            "type": issue.get("type", "Unknown"),
            "severity": severity,
            "line": issue.get("line", 1),
            "confidence": issue.get("confidence", 0) / 100,
            "risk_score": risk_scores.get(severity, 3),
            "description": issue.get(
                "description",
                "Potential security vulnerability detected."
            ),
            "recommendation": issue.get(
                "recommendation",
                "Review and fix the identified security issue."
            )
        })

    overall_risk = calculate_overall_risk(issues)

    return {
        "success": True,
        "total_vulnerabilities": len(vulnerabilities),
        "vulnerabilities": vulnerabilities,
        "overall_risk": overall_risk,
        "source": "backend"
    }