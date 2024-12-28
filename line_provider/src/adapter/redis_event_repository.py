import json
from datetime import datetime
from typing import List, Optional

from redis.asyncio import Redis
from src.domain.event_model import Event
from src.domain.event_repository import EventRepository


class RedisEventRepository(EventRepository):
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def get_event(self, event_id: str) -> Optional[Event]:
        key = f"event:{event_id}"
        event_data = await self.redis.get(key)
        if event_data:
            event_dict = json.loads(event_data)
            return Event(**event_dict)
        return None

    async def list_events(self) -> List[Event]:
        pattern = "event:*"
        cursor = 0
        events = []
        current_time = datetime.now().timestamp()
        while True:
            cursor, keys = await self.redis.scan(
                cursor=cursor, match=pattern, count=100
            )
            if keys:
                async with self.redis.pipeline() as pipe:
                    for key in keys:
                        pipe.get(key)
                    events_data = await pipe.execute()
                for event_data in events_data:
                    if event_data:
                        event_dict = json.loads(event_data)
                        if (
                            "deadline" in event_dict
                            and event_dict["deadline"] > current_time
                        ):
                            events.append(Event(**event_dict))
            if cursor == 0:
                break
        return events

    async def create_event(self, event: Event) -> None:
        key = f"event:{event.event_id}"
        event_dict = event.model_dump()
        event_json = json.dumps(event_dict)
        await self.redis.set(key, event_json)

    async def update_event(self, event: Event) -> None:
        key = f"event:{event.event_id}"
        exists = await self.redis.exists(key)
        if exists:
            event_dict = event.model_dump()
            event_json = json.dumps(event_dict)
            await self.redis.set(key, event_json)

    async def delete_event(self, event_id: str) -> None:
        key = f"event:{event_id}"
        return await self.redis.delete(key)
