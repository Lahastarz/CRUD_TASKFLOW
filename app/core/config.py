from functools import lru_cache
from typing import Literal

from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- App ---
    ENVIRONMENT: Literal['local', 'staging', 'production'] = 'local'
    DEBUG: bool = False
    PROJECT_NAME: str = "Taskflow CRUD"

    # --- Database ---
    DATABASE_URL: PostgresDsn
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 5

    # --- Redis ---
    REDIS_URL: RedisDsn

    # --- JWT / Auth ---
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: Literal["HS256", "RS256"] = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- OTP ---
    OTP_LENGTH: int = 6
    OTP_TTL_SECONDS: int = 300  # 5 minutes
    OTP_MAX_ATTEMPTS: int = 5

    # --- Rate limiting ---
    LOGIN_RATE_LIMIT: str = "5/minute"
    OTP_RATE_LIMIT: str = "3/minute"

    # --- CORS ---
    ALLOWED_ORIGINS: list[str] = ["http://localhost:8080"]

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def secret_key_not_default(cls, v:str)->str:
        if v in {"changeme", "secret", "your-secret-key"}:
            raise ValueError(
                "JWT_SECRET_KEY is set to an insecure placeholder. "
                "Generate one with: python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        return v
    
@lru_cache
def get_settings()-> Settings:
    return Settings()

settings= get_settings()