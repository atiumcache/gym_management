from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Gym Management API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    debug: bool = False

    # Database
    DATABASE_URL: str = "postgresql://test:test@localhost:5433/test"

    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change this to a secure secret key
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
