from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    DATABASE_URL: str = (
        "postgresql+asyncpg://projectalpha_user:projectalpha_pass@localhost:5432/projectalpha"
    )
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = os.getenv("ENV_FILE", ".env")
        case_sensitive = True

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


settings = Settings()
