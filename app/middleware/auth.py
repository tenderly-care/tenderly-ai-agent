"""Authentication middleware for JWT and API key validation."""

from typing import Optional
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config.settings import settings
from app.utils.logger import get_logger
from app.exceptions.custom_exceptions import AuthenticationError
from app.middleware.api_key_auth import get_api_key_auth, get_api_key_auth_optional

logger = get_logger(__name__)
security = HTTPBearer()


def verify_jwt_token(token: str) -> dict:
    """
    Verify JWT token and return payload.
    
    Args:
        token: JWT token string
        
    Returns:
        Token payload dictionary
        
    Raises:
        AuthenticationError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
            options={"verify_aud": False}  # Disable audience verification for backend compatibility
        )
        
        # Check if token has required fields
        if not payload.get("sub"):
            raise AuthenticationError("Token missing subject")
            
        return payload
        
    except JWTError as e:
        logger.error(f"JWT token validation failed: {e}")
        raise AuthenticationError(f"Invalid token: {e}")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Get current user from JWT token.
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        User information from token payload
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        payload = verify_jwt_token(credentials.credentials)
        return payload
        
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


# Hybrid authentication: API Key (preferred) or JWT (legacy)
async def get_current_user_hybrid(request: Request) -> dict:
    """
    Get current authenticated user/service using API key (preferred) or JWT (legacy).
    
    Args:
        request: FastAPI request object
        
    Returns:
        User/service information
        
    Raises:
        HTTPException: If authentication fails
    """
    # Try API key authentication first (preferred for service-to-service)
    api_key = request.headers.get(settings.api_key_header_name)
    if api_key:
        try:
            auth_info = await get_api_key_auth(request)
            # Convert to user-like format for backward compatibility
            return {
                "sub": auth_info.get("service", "unknown"),
                "service_name": auth_info.get("service"),
                "authenticated": auth_info.get("authenticated", False),
                "auth_type": "api_key",
                "metadata": {
                    "request_id": request.headers.get("X-Request-ID"),
                    "session_id": request.headers.get("X-Session-ID"),
                    "patient_id": request.headers.get("X-Patient-ID"),
                    "client_ip": getattr(request.client, 'host', None) if request.client else None,
                }
            }
        except HTTPException:
            # If API key auth fails, don't fall back to JWT
            raise
    
    # Fall back to JWT authentication (legacy)
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_jwt_token(token)
            payload["auth_type"] = "jwt"
            return payload
        except AuthenticationError as e:
            logger.error(f"JWT authentication failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    # No valid authentication found
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No valid authentication provided. Use X-API-Key header or Bearer token.",
        headers={"WWW-Authenticate": "ApiKey, Bearer"},
    )


# Update the main get_current_user to use hybrid authentication
async def get_current_user_new(request: Request) -> dict:
    """
    Get current authenticated user/service (API key preferred, JWT fallback).
    
    Args:
        request: FastAPI request object
        
    Returns:
        User/service information
        
    Raises:
        HTTPException: If authentication fails
    """
    return await get_current_user_hybrid(request)


# Optional authentication dependency for health checks
async def get_current_user_optional(
    request: Request
) -> Optional[dict]:
    """
    Get current user from API key or JWT token (optional).
    
    Args:
        request: FastAPI request object
        
    Returns:
        User information from token payload or None
    """
    try:
        return await get_current_user_hybrid(request)
    except HTTPException:
        return None


# Legacy JWT-only authentication (for backward compatibility)
async def get_current_user_jwt_only(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Get current user from JWT token only (legacy).
    
    Args:
        credentials: HTTP authorization credentials
        
    Returns:
        User information from token payload
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        payload = verify_jwt_token(credentials.credentials)
        return payload
        
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


# Alias for backward compatibility - now uses hybrid auth
get_current_user = get_current_user_new
