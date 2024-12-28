import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_LINE_PROVIDER_HOST: str = os.getenv("REDIS_LINE_PROVIDER_HOST", "localhost")
    REDIS_LINE_PROVIDER_PORT: int = int(os.getenv("REDIS_LINE_PROVIDER_PORT", "6380"))
    REDIS_LINE_PROVIDER_DB: int = int(os.getenv("REDIS_LINE_PROVIDER_DB", "0"))
    REDIS_LINE_PROVIDER_PASSWORD: str = os.getenv("REDIS_LINE_PROVIDER_PASSWORD", "")
    LINE_PROVIDER_PORT: int = os.getenv("LINE_PROVIDER_PORT", "8001")
    BET_SERVICE_CALLBACK_URL: str = os.getenv("BET_SERVICE_CALLBACK_URL")

    class Config:
        env_file = ".env"


settings = Settings()
