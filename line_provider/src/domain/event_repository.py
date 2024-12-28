from abc import ABC, abstractmethod
from typing import List

from src.domain.event_model import Event


class EventRepository(ABC):
    @abstractmethod
    async def get_event(self, event_id: str) -> Event:
        pass

    @abstractmethod
    async def list_events(self) -> List[Event]:
        pass

    @abstractmethod
    async def create_event(self, event: Event) -> None:
        pass

    @abstractmethod
    async def update_event(self, event: Event) -> None:
        pass

    @abstractmethod
    async def delete_event(self, event_id: str) -> None:
        pass
