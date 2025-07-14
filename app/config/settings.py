"""Application configuration settings."""

import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """Application settings."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    openai_max_tokens: int = 1000
    openai_temperature: float = 0.1

    # Application Configuration
    app_name: str = "Tenderly AI Agent"
    app_version: str = "1.0.0"
    app_description: str = "AI Diagnosis Agent for Gynecology Care"
    debug: bool = False
    log_level: str = "INFO"
    environment: str = "production"

    # Security Configuration
    secret_key: str
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    cors_origins: List[str] = ["http://localhost:3000", "https://tenderly.care"]

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 3600

    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None
    redis_ssl: bool = False

    # API Configuration
    api_prefix: str = "/api/v1"
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # Medical Disclaimer
    medical_disclaimer: str = (
        "This diagnosis is AI-generated and should not replace professional "
        "medical consultation. Always consult with a qualified healthcare provider for medical advice."
    )

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

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
