"""Rate limiting middleware."""

import time
from typing import Optional
import redis.asyncio as redis
from fastapi import Request, HTTPException, status
from app.config.settings import settings
from app.utils.logger import get_logger
from app.exceptions.custom_exceptions import RateLimitError

logger = get_logger(__name__)


class RateLimiter:
    """Redis-based rate limiter."""
    
    def __init__(self):
        """Initialize rate limiter."""
        self.redis_client: Optional[redis.Redis] = None
        self.requests_limit = settings.rate_limit_requests
        self.window_seconds = settings.rate_limit_window
    
    async def init_redis(self):
        """Initialize Redis connection."""
        if not self.redis_client:
            try:
                self.redis_client = redis.from_url(settings.redis_url)
                await self.redis_client.ping()
                logger.info("Redis connection established for rate limiting")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {e}")
                self.redis_client = None
    
    async def check_rate_limit(self, request: Request, user_id: str = None) -> bool:
        """
        Check if request is within rate limit.
        
        Args:
            request: FastAPI request object
            user_id: Optional user ID for user-specific rate limiting
            
        Returns:
            True if within rate limit, False otherwise
            
        Raises:
            RateLimitError: If rate limit exceeded
        """
        if not self.redis_client:
            await self.init_redis()
            
        if not self.redis_client:
            # If Redis is not available, allow all requests
            logger.warning("Redis unavailable, skipping rate limiting")
            return True
        
        # Create rate limit key
        identifier = user_id or request.client.host
        key = f"rate_limit:{identifier}"
        
        try:
            current_time = int(time.time())
            window_start = current_time - self.window_seconds
            
            # Remove old entries
            await self.redis_client.zremrangebyscore(key, 0, window_start)
            
            # Count current requests
            current_requests = await self.redis_client.zcard(key)
            
            if current_requests >= self.requests_limit:
                logger.warning(f"Rate limit exceeded for {identifier}")
                raise RateLimitError(
                    f"Rate limit exceeded. Maximum {self.requests_limit} requests per {self.window_seconds} seconds"
                )
            
            # Add current request
            await self.redis_client.zadd(key, {str(current_time): current_time})
            
            # Set expiration
            await self.redis_client.expire(key, self.window_seconds)
            
            return True
            
        except RateLimitError:
            raise
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            # If rate limiting fails, allow the request
            return True
    
    async def get_rate_limit_info(self, request: Request, user_id: str = None) -> dict:
        """
        Get rate limit information for a user/IP.
        
        Args:
            request: FastAPI request object
            user_id: Optional user ID
            
        Returns:
            Dictionary with rate limit information
        """
        if not self.redis_client:
            await self.init_redis()
            
        if not self.redis_client:
            return {
                "limit": self.requests_limit,
                "window": self.window_seconds,
                "remaining": self.requests_limit,
                "reset_time": int(time.time()) + self.window_seconds
            }
        
        identifier = user_id or request.client.host
        key = f"rate_limit:{identifier}"
        
        try:
            current_time = int(time.time())
            window_start = current_time - self.window_seconds
            
            # Remove old entries
            await self.redis_client.zremrangebyscore(key, 0, window_start)
            
            # Count current requests
            current_requests = await self.redis_client.zcard(key)
            remaining = max(0, self.requests_limit - current_requests)
            
            return {
                "limit": self.requests_limit,
                "window": self.window_seconds,
                "remaining": remaining,
                "reset_time": current_time + self.window_seconds
            }
            
        except Exception as e:
            logger.error(f"Failed to get rate limit info: {e}")
            return {
                "limit": self.requests_limit,
                "window": self.window_seconds,
                "remaining": self.requests_limit,
                "reset_time": int(time.time()) + self.window_seconds
            }


# Global rate limiter instance
rate_limiter = RateLimiter()


async def check_rate_limit_dependency(request: Request, user: dict = None):
    """
    FastAPI dependency for rate limiting.
    
    Args:
        request: FastAPI request object
        user: Optional user information
        
    Raises:
        HTTPException: If rate limit exceeded
    """
    try:
        user_id = user.get("sub") if user else None
        await rate_limiter.check_rate_limit(request, user_id)
    except RateLimitError as e:
        logger.warning(f"Rate limit exceeded: {e}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=str(e),
            headers={"Retry-After": str(settings.rate_limit_window)}
        )
