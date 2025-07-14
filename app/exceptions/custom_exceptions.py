"""Custom exceptions for the application."""


class BaseCustomException(Exception):
    """Base exception class for custom exceptions."""
    
    def __init__(self, message: str, error_code: str = None):
        """Initialize base exception."""
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class OpenAIServiceError(BaseCustomException):
    """Exception raised when OpenAI service fails."""
    
    def __init__(self, message: str):
        """Initialize OpenAI service error."""
        super().__init__(message, "OPENAI_SERVICE_ERROR")


class DiagnosisServiceError(BaseCustomException):
    """Exception raised when diagnosis service fails."""
    
    def __init__(self, message: str):
        """Initialize diagnosis service error."""
        super().__init__(message, "DIAGNOSIS_SERVICE_ERROR")


class AuthenticationError(BaseCustomException):
    """Exception raised when authentication fails."""
    
    def __init__(self, message: str):
        """Initialize authentication error."""
        super().__init__(message, "AUTHENTICATION_ERROR")


class RateLimitError(BaseCustomException):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(self, message: str):
        """Initialize rate limit error."""
        super().__init__(message, "RATE_LIMIT_ERROR")


class ValidationError(BaseCustomException):
    """Exception raised when validation fails."""
    
    def __init__(self, message: str):
        """Initialize validation error."""
        super().__init__(message, "VALIDATION_ERROR")
