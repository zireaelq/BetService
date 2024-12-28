import httpx
from fastapi import Depends
from redis.asyncio import Redis
from src.adapter.redis_client import get_redis_client
from src.adapter.redis_event_repository import RedisEventRepository
from src.application.event import EventService


async def get_event_service(
    redis_client: Redis = Depends(get_redis_client),
) -> EventService:
    repository = RedisEventRepository(redis_client)
    return EventService(repository)


async def get_httpx_client():
    async with httpx.AsyncClient() as client:
        yield client
