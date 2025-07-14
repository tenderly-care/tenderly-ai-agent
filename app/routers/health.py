"""Health check router for service monitoring."""

from fastapi import APIRouter, Depends, status
from app.models import HealthCheckResponse
from app.services.openai_service import openai_service
from app.middleware.rate_limiter import rate_limiter
from app.middleware.auth import get_current_user_optional
from app.config.settings import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check the health status of the AI diagnosis service",
)
async def health_check(
    current_user: dict = Depends(get_current_user_optional),
) -> HealthCheckResponse:
    """
    Check the health status of the AI diagnosis service.
    
    Args:
        current_user: Optional current user information
        
    Returns:
        Health check response with service status
    """
    try:
        # Check external services
        services_status = {}
        
        # Check OpenAI service
        try:
            openai_healthy = await openai_service.health_check()
            services_status["openai"] = "healthy" if openai_healthy else "unhealthy"
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            services_status["openai"] = "unhealthy"
        
        # Check Redis service
        try:
            await rate_limiter.init_redis()
            if rate_limiter.redis_client:
                await rate_limiter.redis_client.ping()
                services_status["redis"] = "healthy"
            else:
                services_status["redis"] = "unhealthy"
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            services_status["redis"] = "unhealthy"
        
        # Determine overall status
        overall_status = "healthy"
        if services_status.get("openai") == "unhealthy":
            overall_status = "degraded"  # OpenAI is critical
        elif services_status.get("redis") == "unhealthy":
            overall_status = "degraded"  # Redis is important but not critical
        
        logger.info(
            f"Health check completed",
            extra={
                "status": overall_status,
                "services": services_status,
                "user_id": current_user.get("sub") if current_user else None,
            }
        )
        
        return HealthCheckResponse(
            status=overall_status,
            version=settings.app_version,
            services=services_status,
        )
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthCheckResponse(
            status="unhealthy",
            version=settings.app_version,
            services={"error": str(e)},
        )


@router.get(
    "/live",
    status_code=status.HTTP_200_OK,
    summary="Liveness probe",
    description="Simple liveness probe for Kubernetes",
)
async def liveness_probe() -> dict:
    """
    Simple liveness probe for Kubernetes.
    
    Returns:
        Simple status response
    """
    return {"status": "alive"}


@router.get(
    "/ready",
    status_code=status.HTTP_200_OK,
    summary="Readiness probe",
    description="Readiness probe for Kubernetes",
)
async def readiness_probe() -> dict:
    """
    Readiness probe for Kubernetes.
    
    Returns:
        Readiness status response
    """
    try:
        # Check if OpenAI service is accessible
        openai_healthy = await openai_service.health_check()
        
        if openai_healthy:
            return {"status": "ready"}
        else:
            return {"status": "not_ready", "reason": "OpenAI service unavailable"}
            
    except Exception as e:
        logger.error(f"Readiness probe failed: {e}")
        return {"status": "not_ready", "reason": str(e)}
