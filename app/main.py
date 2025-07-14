"""Main FastAPI application."""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.config.settings import settings
from app.routers import diagnosis_router, health_router
from app.utils.logger import get_logger, setup_logging
from app.exceptions.custom_exceptions import (
    BaseCustomException,
    OpenAIServiceError,
    DiagnosisServiceError,
    AuthenticationError,
    RateLimitError,
)

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    logger.info("Starting Tenderly AI Agent service")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Tenderly AI Agent service")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# Exception handlers
@app.exception_handler(BaseCustomException)
async def custom_exception_handler(request: Request, exc: BaseCustomException):
    """Handle custom exceptions."""
    logger.error(f"Custom exception: {exc.message}")
    
    status_code = 500
    if isinstance(exc, AuthenticationError):
        status_code = 401
    elif isinstance(exc, RateLimitError):
        status_code = 429
    elif isinstance(exc, (OpenAIServiceError, DiagnosisServiceError)):
        status_code = 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "timestamp": str(request.state.timestamp) if hasattr(request.state, 'timestamp') else None,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.error(f"Validation error: {exc.errors()}")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "detail": exc.errors(),
            "timestamp": str(request.state.timestamp) if hasattr(request.state, 'timestamp') else None,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {exc}")
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "An unexpected error occurred",
            "detail": str(exc) if settings.debug else "Internal server error",
            "timestamp": str(request.state.timestamp) if hasattr(request.state, 'timestamp') else None,
        },
    )


# Request middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request processing time header."""
    import time
    from datetime import datetime
    
    start_time = time.time()
    request.state.timestamp = datetime.utcnow()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    
    return response


# Include routers
app.include_router(health_router, prefix=settings.api_prefix)
app.include_router(diagnosis_router, prefix=settings.api_prefix)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Tenderly AI Agent - Gynecology Diagnosis Service",
        "version": settings.app_version,
        "status": "healthy",
        "docs_url": "/docs" if settings.debug else None,
    }


# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        workers=1 if settings.debug else settings.workers,
        log_level=settings.log_level.lower(),
    )
