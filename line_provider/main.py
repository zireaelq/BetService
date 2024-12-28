from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from src.adapter.redis_client import get_redis_client
from src.api.routes import event_router

app = FastAPI(
    title="Line Provider service"
)


@app.on_event("startup")
async def on_startup():
    async for redis in get_redis_client():
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


app.include_router(event_router.router, prefix="/api", tags=["Events"])
