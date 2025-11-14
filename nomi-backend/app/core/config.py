"""Application configuration loaded from environment variables."""

import os
from typing import List

from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str = Field(
        default="postgresql+asyncpg://nomi:nomi@db:5432/nomi",
        alias="DATABASE_URL",
        description="PostgreSQL connection string with asyncpg driver",
    )

    # Microsoft Entra ID (Azure AD) Configuration
    entraid_client_id: str = Field(default="", alias="ENTRAID_CLIENT_ID")
    entraid_tenant_id: str = Field(default="", alias="ENTRAID_TENANT_ID")
    entraid_client_secret: str = Field(default="", alias="ENTRAID_CLIENT_SECRET")
    entraid_redirect_uri: str = Field(
        default="http://localhost:8000/api/auth/callback",
        alias="ENTRAID_REDIRECT_URI",
    )

    # Session Configuration
    session_secret_key: str = Field(
        default="dev-secret-key-change-in-production",
        alias="SESSION_SECRET_KEY",
    )
    session_cookie_name: str = Field(default="nomi_session", alias="SESSION_COOKIE_NAME")
    session_max_age: int = Field(default=86400, alias="SESSION_MAX_AGE")

    # Application Settings
    environment: str = Field(default="development", alias="ENVIRONMENT")
    debug: bool = Field(default=True, alias="DEBUG")
    cors_origins: List[str] = Field(
        default=["http://localhost:5173"],
        alias="CORS_ORIGINS",
    )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_prefix="",
    )

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"


# Global settings instance
settings = Settings()
