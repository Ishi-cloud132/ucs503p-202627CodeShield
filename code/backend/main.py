from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from analyzers.static_analyzer import analyze_code
from services.risk_assessment import calculate_overall_risk

# CodeShield ML
from codeshield_ml.model import assess_code


app = FastAPI(
    title="CodeShield API",
    description="Code vulnerability detection and risk assessment API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

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


# ============================================================
# BASIC ROUTES
# ============================================================

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


# ============================================================
# CODE SCANNING
# ============================================================

@app.post("/scan")
def scan_code(data: dict):

    code = data.get("code", "")

    if not code.strip():
        return {
            "success": False,
            "message": "No code provided",
            "total_vulnerabilities": 0,
            "vulnerabilities": [],
            "ml_assessment": None
        }

    # ========================================================
    # 1. STATIC ANALYSIS
    # ========================================================

    issues = analyze_code(code)

    vulnerabilities = []

    risk_scores = {
        "NONE": 0,
        "LOW": 3,
        "MEDIUM": 6,
        "HIGH": 9,
        "CRITICAL": 10
    }

    for issue in issues:

        severity = issue.get("severity", "LOW").upper()

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
            ),

            "detection_method": "static"
        })


    # ========================================================
    # 2. MACHINE LEARNING ANALYSIS
    # ========================================================

    ml_assessment = assess_code(code)


    # ========================================================
    # 3. ADD ML FINDING IF VULNERABILITY DETECTED
    # ========================================================

    if ml_assessment is not None:

        ml_type = ml_assessment.get("vulnerability_type")

        # Only add the ML result to vulnerabilities if the
        # classifier believes the code is actually vulnerable.
        if ml_assessment.get("is_vulnerable"):

            # Avoid adding an obvious duplicate if the static
            # analyzer already detected the same vulnerability.
            already_detected = any(
                v.get("type") == ml_type
                for v in vulnerabilities
            )

            if not already_detected:

                vulnerabilities.append({
                    "type": ml_type,
                    "severity": ml_assessment.get(
                        "severity",
                        "UNKNOWN"
                    ),
                    "line": None,
                    "confidence": ml_assessment.get(
                        "confidence",
                        0
                    ),
                    "risk_score": ml_assessment.get(
                        "risk_score",
                        0
                    ),
                    "cwe": ml_assessment.get("cwe"),

                    "description": (
                        f"Machine learning classifier detected "
                        f"potential {ml_type}."
                    ),

                    "recommendation": (
                        "Review the affected code and verify "
                        "the detected vulnerability."
                    ),

                    "detection_method": "ml"
                })


    # ========================================================
    # 4. OVERALL RISK
    # ========================================================

    overall_risk = calculate_overall_risk(issues)

    if ml_assessment is not None:

        ml_risk = ml_assessment.get("risk_score", 0)

        static_risk_scores = {
            "NONE": 0,
            "LOW": 3,
            "MEDIUM": 6,
            "HIGH": 9,
            "CRITICAL": 10
        }

        static_risk_score = static_risk_scores.get(
            str(overall_risk).upper(),
            0
        )

        if ml_risk > static_risk_score:

            risk_labels = {
                0: "NONE",
                3: "LOW",
                6: "MEDIUM",
                9: "HIGH",
                10: "CRITICAL"
            }

            overall_risk = risk_labels.get(
                ml_risk,
                "HIGH"
            )


    # ========================================================
    # 5. FINAL RESPONSE
    # ========================================================

    return {
        "success": True,

        "total_vulnerabilities": len(
            vulnerabilities
        ),

        "vulnerabilities": vulnerabilities,

        "overall_risk": overall_risk,

        "ml_assessment": ml_assessment,

        "source": "static+ml"
    }