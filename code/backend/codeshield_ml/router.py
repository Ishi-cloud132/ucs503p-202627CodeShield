"""FastAPI routes for optional ML-assisted scans."""

from fastapi import APIRouter
from pydantic import BaseModel

from .scan_service import scan_code

router = APIRouter(prefix="/ml", tags=["machine learning"])


class ScanRequest(BaseModel):
    code: str = ""


@router.post("/scan")
def scan(request: ScanRequest) -> dict:
    if not request.code.strip():
        return {
            "success": False,
            "message": "No code provided",
            "total_vulnerabilities": 0,
            "vulnerabilities": [],
            "ml_assessment": None,
            "source": "static",
        }
    return scan_code(request.code)