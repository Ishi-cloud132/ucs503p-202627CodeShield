"""Explicit opt-in integration for the existing FastAPI application."""

from fastapi import FastAPI

from .router import router


def register_codeshield_ml(app: FastAPI) -> None:
    """Register the ML routes without changing the host application's routes."""
    app.include_router(router)