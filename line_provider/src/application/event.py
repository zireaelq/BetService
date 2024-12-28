from typing import List, Optional

from src.domain.event_model import CreateEvent, Event, EventStatus
from src.domain.event_repository import EventRepository


class EventService:
    def __init__(self, repository: EventRepository):
        self.repository = repository

    async def get_event(self, event_id: str) -> Optional[Event]:
        return await self.repository.get_event(event_id)

    async def list_events(self) -> List[Event]:
        return await self.repository.list_events()

    async def create_event(self, event: CreateEvent) -> None:
        existing_event = await self.repository.get_event(event.event_id)
        if existing_event:
            raise ValueError("Event with this ID already exists.")
        await self.repository.create_event(event)

    async def update_event_status(self, event_id: str, new_status: EventStatus) -> None:
        event = await self.repository.get_event(event_id)
        if event:
            event.status = new_status
            await self.repository.update_event(event)
        else:
            raise ValueError("Event not found.")

    async def delete_event(self, event_id: str) -> None:
        return await self.repository.delete_event(event_id)
