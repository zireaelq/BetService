import httpx
from fastapi import Depends
from redis.asyncio import Redis
from src.adapter.redis_bet_repository import RedisBetRepository
from src.adapter.redis_client import get_redis_client
from src.application.bet import BetService


async def get_bet_service(
    redis_client: Redis = Depends(get_redis_client),
) -> BetService:
    repository = RedisBetRepository(redis_client)
    return BetService(repository)


async def get_httpx_client():
    async with httpx.AsyncClient() as client:
        yield client
