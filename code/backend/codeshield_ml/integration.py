"""Explicit opt-in integration for the existing FastAPI application."""

from fastapi import FastAPI

from .router import router


def register_codeshield_ml(app: FastAPI) -> None:
    """Register the CodeShield ML scan routes."""
    app.include_router(router)
