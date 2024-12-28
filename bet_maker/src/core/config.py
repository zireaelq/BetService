import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_BET_MAKER_HOST: str = os.getenv("REDIS_BET_MAKER_HOST", "localhost")
    REDIS_BET_MAKER_PORT: int = int(os.getenv("REDIS_BET_MAKER_PORT", "6380"))
    REDIS_BET_MAKER_DB: int = int(os.getenv("REDIS_BET_MAKER_DB", "0"))
    REDIS_BET_MAKER_PASSWORD: str = os.getenv("REDIS_BET_MAKER_PASSWORD", "")
    BET_MAKER_PORT: int = os.getenv("BET_MAKER_PORT", "8001")
    EVENT_SERVICE_URL: str = os.getenv("EVENT_SERVICE_URL")

    class Config:
        env_file = ".env"


settings = Settings()
