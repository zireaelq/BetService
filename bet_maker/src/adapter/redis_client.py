from typing import AsyncGenerator
from redis.asyncio import Redis
from src.core.config import settings

async def get_redis_client() -> AsyncGenerator[Redis, None]:
    client = Redis(
        host=settings.REDIS_BET_MAKER_HOST,
        port=settings.REDIS_BET_MAKER_PORT,
        db=settings.REDIS_BET_MAKER_DB,
        password=settings.REDIS_BET_MAKER_PASSWORD or None,
        decode_responses=True
    )
    try:
        yield client
    finally:
        await client.close()
