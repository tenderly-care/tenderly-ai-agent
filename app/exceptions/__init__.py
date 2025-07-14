"""Exceptions module."""

from .custom_exceptions import (
    BaseCustomException,
    OpenAIServiceError,
    DiagnosisServiceError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
)

__all__ = [
    "BaseCustomException",
    "OpenAIServiceError",
    "DiagnosisServiceError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
]
