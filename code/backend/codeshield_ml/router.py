"""FastAPI routes for CodeShield hybrid static + ML scans."""

from fastapi import APIRouter
from pydantic import BaseModel

from .scan_service import scan_code


router = APIRouter(prefix="/ml", tags=["machine learning"])


class ScanRequest(BaseModel):
    code: str = ""


@router.post("/scan")
def scan(request: ScanRequest) -> dict:
    """Scan submitted source code using static rules + ML."""
    if not request.code.strip():
        return {
            "success": False,
            "message": "No code provided",
            "total_vulnerabilities": 0,
            "vulnerabilities": [],
            "overall_risk": 0,
            "ml_assessment": None,
            "source": "static",
        }

    return scan_code(request.code)
