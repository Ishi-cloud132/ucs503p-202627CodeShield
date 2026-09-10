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
            "issues": []
        }

    issues = analyze_code(code)

    overall_risk = calculate_overall_risk(issues)

    return {
        "success": True,
        "total_issues": len(issues),
        "overall_risk": overall_risk,
        "issues": issues
    }