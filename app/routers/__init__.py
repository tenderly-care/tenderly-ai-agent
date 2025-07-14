"""Routers module."""

from .diagnosis import router as diagnosis_router
from .health import router as health_router

__all__ = ["diagnosis_router", "health_router"]
