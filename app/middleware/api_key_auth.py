"""API Key authentication middleware for service-to-service communication."""

from typing import Optional
from fastapi import HTTPException, status, Depends, Request
from app.config.settings import settings
from app.utils.logger import get_logger
from app.exceptions.custom_exceptions import AuthenticationError

logger = get_logger(__name__)

def verify_api_key(api_key: str, service_name: Optional[str] = None) -> dict:
    """
    Verify API key and return service information.
    
    Args:
        api_key: API key string
        service_name: Optional service name for additional validation
        
    Returns:
        Service information dictionary
        
    Raises:
        AuthenticationError: If API key is invalid
    """
    try:
        # Check if API key matches the configured key
        if not api_key or api_key != settings.api_key:
            raise AuthenticationError("Invalid API key")
        
        # Optional: Validate service name if provided
        allowed_services = settings.allowed_services_list
        if service_name and service_name not in allowed_services:
            logger.warning(f"Request from unauthorized service: {service_name}")
            # For now, we'll allow it but log it
            
        return {
            "service": service_name or "unknown",
            "authenticated": True,
            "api_key_valid": True,
        }
        
    except Exception as e:
        logger.error(f"API key validation failed: {e}")
        raise AuthenticationError(f"Authentication failed: {e}")


async def get_api_key_auth(request: Request) -> dict:
    """
    Get API key authentication from request headers.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Service authentication information
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Get API key from request headers
        api_key = request.headers.get(settings.api_key_header_name)
        
        if not api_key:
            logger.error("Missing API key in request headers")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing API key. Please provide the correct header.",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        # Get optional service name
        service_name = request.headers.get("X-Service-Name")
        
        # Verify API key
        auth_info = verify_api_key(api_key, service_name)
        
        logger.info(
            f"API key authentication successful",
            extra={
                "service": auth_info.get("service"),
            }
        )
        
        return auth_info
        
    except HTTPException:
        raise
    except AuthenticationError as e:
        logger.error(f"API key authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "ApiKey"},
        )
    except Exception as e:
        logger.error(f"Unexpected authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service error",
        )

# Optional authentication dependency for health checks
async def get_api_key_auth_optional(request: Request) -> Optional[dict]:
    """
    Get API key authentication from request headers (optional).
    
    Args:
        request: FastAPI request object
        
    Returns:
        Service authentication information or None
    """
    try:
        return await get_api_key_auth(request)
    except HTTPException:
        return None
