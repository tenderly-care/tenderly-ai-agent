"""Authentication middleware for JWT token validation."""

from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.config.settings import settings
from app.utils.logger import get_logger
from app.exceptions.custom_exceptions import AuthenticationError

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
            algorithms=[settings.jwt_algorithm]
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


# Optional authentication dependency for health checks
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[dict]:
    """
    Get current user from JWT token (optional).
    
    Args:
        credentials: HTTP authorization credentials (optional)
        
    Returns:
        User information from token payload or None
    """
    if not credentials:
        return None
        
    try:
        payload = verify_jwt_token(credentials.credentials)
        return payload
        
    except AuthenticationError:
        return None
