import time
from typing import List
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from src.application.event import EventService
from src.domain.event_model import Event, EventStatus
from src.domain.event_repository import EventRepository


@pytest.fixture
def mock_repository() -> AsyncMock:
    return AsyncMock(spec=EventRepository)


@pytest.fixture
def event_service(mock_repository: AsyncMock) -> EventService:
    return EventService(repository=mock_repository)


@pytest.mark.asyncio
async def test_get_event(event_service: EventService, mock_repository: AsyncMock):
    event_id = uuid4().hex
    expected_event = Event(
        event_id=event_id,
        coefficient=1.5,
        deadline=int(time.mktime((2026, 1, 1, 0, 0, 0, 0, 0, 0))),
        status=EventStatus.NEW,
    )
    mock_repository.get_event.return_value = expected_event

    result = await event_service.get_event(event_id)

    assert result == expected_event
    mock_repository.get_event.assert_awaited_once_with(event_id)


@pytest.mark.asyncio
async def test_list_events(event_service: EventService, mock_repository: AsyncMock):
    expected_events: List[Event] = [
        Event(
            event_id=uuid4().hex,
            coefficient=1.2,
            deadline=int(time.mktime((2026, 1, 1, 0, 0, 0, 0, 0, 0))),
            status=EventStatus.NEW,
        ),
        Event(
            event_id=uuid4().hex,
            coefficient=2.0,
            deadline=int(time.mktime((2026, 1, 1, 0, 0, 0, 0, 0, 0))),
            status=EventStatus.FINISHED_WIN,
        ),
    ]
    mock_repository.list_events.return_value = expected_events

    result = await event_service.list_events()

    assert result == expected_events
    mock_repository.list_events.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_event_success(
    event_service: EventService, mock_repository: AsyncMock
):
    new_event = Event(
        event_id=uuid4().hex,
        coefficient=1.5,
        deadline=int(time.mktime((2026, 1, 1, 0, 0, 0, 0, 0, 0))),
        status=EventStatus.NEW,
    )
    mock_repository.get_event.return_value = None

    await event_service.create_event(new_event)

    mock_repository.create_event.assert_awaited_once_with(new_event)


@pytest.mark.asyncio
async def test_create_event_duplicate(
    event_service: EventService, mock_repository: AsyncMock
):
    new_event = Event(
        event_id=uuid4().hex,
        coefficient=1.5,
        deadline=int(time.mktime((2026, 1, 1, 0, 0, 0, 0, 0, 0))),
        status=EventStatus.NEW,
    )
    mock_repository.get_event.return_value = new_event

    with pytest.raises(ValueError, match="Event with this ID already exists."):
        await event_service.create_event(new_event)


@pytest.mark.asyncio
async def test_update_event_status_success(
    event_service: EventService, mock_repository: AsyncMock
):
    event_id = uuid4().hex
    existing_event = Event(
        event_id=event_id,
        coefficient=1.5,
        deadline=int(time.mktime((2026, 1, 1, 0, 0, 0, 0, 0, 0))),
        status=EventStatus.NEW,
    )
    mock_repository.get_event.return_value = existing_event
    new_status = EventStatus.FINISHED_WIN

    await event_service.update_event_status(event_id, new_status)

    assert existing_event.status == new_status
    mock_repository.update_event.assert_awaited_once_with(existing_event)


@pytest.mark.asyncio
async def test_update_event_status_not_found(
    event_service: EventService, mock_repository: AsyncMock
):
    event_id = uuid4().hex
    mock_repository.get_event.return_value = None

    with pytest.raises(ValueError, match="Event not found."):
        await event_service.update_event_status(event_id, EventStatus.FINISHED_WIN)


@pytest.mark.asyncio
async def test_delete_event(event_service: EventService, mock_repository: AsyncMock):
    event_id = uuid4().hex

    await event_service.delete_event(event_id)

    mock_repository.delete_event.assert_awaited_once_with(event_id)
