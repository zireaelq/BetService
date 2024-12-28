from typing import AsyncGenerator

from redis.asyncio import Redis
from src.core.config import settings


async def get_redis_client() -> AsyncGenerator[Redis, None]:
    client = Redis(
        host=settings.REDIS_LINE_PROVIDER_HOST,
        port=settings.REDIS_LINE_PROVIDER_PORT,
        db=settings.REDIS_LINE_PROVIDER_DB,
        password=settings.REDIS_LINE_PROVIDER_PASSWORD or None,
        decode_responses=True,
    )
    try:
        yield client
    finally:
        await client.close()
