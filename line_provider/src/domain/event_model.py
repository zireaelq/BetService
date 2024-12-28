from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class EventStatus(str, Enum):
    NEW = "NEW"
    FINISHED_WIN = "FINISHED_WIN"
    FINISHED_LOSE = "FINISHED_LOSE"


class Event(BaseModel):
    event_id: str = Field(default_factory=lambda: uuid4().hex)
    coefficient: float
    deadline: int = Field(gt=0)
    status: EventStatus


class CreateEvent(BaseModel):
    coefficient: float
    deadline: int = Field(gt=0)
    status: EventStatus = EventStatus.NEW
