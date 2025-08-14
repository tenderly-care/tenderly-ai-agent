"""Application configuration settings."""

import os
from typing import List, Optional, Union
from pydantic_settings import BaseSettings
from pydantic import validator, Field


class Settings(BaseSettings):
    """Application settings with production-level security."""

    # OpenAI Configuration
    openai_api_key: str = Field(..., min_length=1, description="OpenAI API key")
    openai_model: str = Field(default="gpt-3.5-turbo", description="OpenAI model to use")
    openai_max_tokens: int = Field(default=1000, ge=1, le=8000, description="Maximum tokens for OpenAI")
    openai_temperature: float = Field(default=0.1, ge=0.0, le=2.0, description="OpenAI temperature")

    # Application Configuration
    app_name: str = Field(default="Tenderly AI Agent", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    app_description: str = Field(default="AI Diagnosis Agent for Gynecology Care", description="App description")
    debug: bool = Field(default=False, description="Debug mode")
    log_level: str = Field(default="INFO", description="Logging level")
    environment: str = Field(default="production", description="Environment")

    # Security Configuration
    secret_key: str = Field(..., min_length=32, description="Application secret key")
    jwt_secret_key: str = Field(..., min_length=32, description="JWT secret key")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    jwt_expiration_hours: int = Field(default=24, ge=1, le=168, description="JWT expiration hours")
    
    # API Key Authentication (Production)
    api_key: Optional[str] = Field(default=None, min_length=32, description="API key for service authentication")
    allowed_services: str = Field(default="tenderly-backend,tenderly-frontend,tenderly-admin", description="Comma-separated allowed services")
    api_key_header_name: str = Field(default="X-API-Key", description="API key header name")
    require_service_name: bool = Field(default=True, description="Require service name in requests")
    allowed_ips: str = Field(default="127.0.0.1,::1", description="Comma-separated allowed IPs")
    
    # Security Features
    enable_request_signing: bool = Field(default=True, description="Enable HMAC request signing")
    max_request_size: int = Field(default=1048576, description="Maximum request size in bytes (1MB)")
    request_timeout: int = Field(default=30, description="Request timeout in seconds")
    enable_rate_limiting: bool = Field(default=True, description="Enable rate limiting")
    
    cors_origins: str = Field(default="http://localhost:3000,https://tenderly.care", description="Comma-separated CORS origins")

    # Rate Limiting
    rate_limit_requests: int = Field(default=100, ge=1, description="Rate limit requests per window")
    rate_limit_window: int = Field(default=3600, ge=60, description="Rate limit window in seconds")

    # Redis Configuration
    redis_host: str = Field(default="localhost", description="Redis host")
    redis_port: int = Field(default=6379, ge=1, le=65535, description="Redis port")
    redis_db: int = Field(default=0, ge=0, le=15, description="Redis database")
    redis_password: Optional[str] = Field(default=None, description="Redis password")
    redis_ssl: bool = Field(default=False, description="Use Redis SSL")

    # API Configuration
    api_prefix: str = Field(default="/api/v1", description="API prefix")
    host: str = Field(default="0.0.0.0", description="Host to bind")
    port: int = Field(default=8000, ge=1, le=65535, description="Port to bind")
    workers: int = Field(default=4, ge=1, le=32, description="Number of workers")

    # Medical Disclaimer
    medical_disclaimer: str = Field(
        default="This diagnosis is AI-generated and should not replace professional "
                "medical consultation. Always consult with a qualified healthcare provider for medical advice.",
        description="Medical disclaimer text"
    )

    @validator("api_key")
    def validate_api_key(cls, v):
        """Validate API key strength."""
        if v is None:
            return v
        if len(v) < 32:
            raise ValueError("API key must be at least 32 characters long")
        if v == "tenderly-api-key-2024-production-change-this":
            import os
            if os.getenv("ENVIRONMENT", "development") == "production":
                raise ValueError("Default API key must be changed in production")
        return v

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins
    
    @property
    def allowed_services_list(self) -> List[str]:
        """Get allowed services as a list."""
        if isinstance(self.allowed_services, str):
            return [service.strip() for service in self.allowed_services.split(",")]
        return self.allowed_services
    
    @property
    def allowed_ips_list(self) -> List[str]:
        """Get allowed IPs as a list."""
        if isinstance(self.allowed_ips, str):
            return [ip.strip() for ip in self.allowed_ips.split(",")]
        return self.allowed_ips

    @property
    def redis_url(self) -> str:
        """Get Redis connection URL."""
        protocol = "rediss" if self.redis_ssl else "redis"
        auth = f":{self.redis_password}@" if self.redis_password else ""
        return f"{protocol}://{auth}{self.redis_host}:{self.redis_port}/{self.redis_db}"

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
