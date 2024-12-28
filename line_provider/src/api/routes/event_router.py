from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from src.api.deps import get_event_service, get_httpx_client
from src.application.event import EventService
from src.core.config import settings
from src.domain.event_model import CreateEvent, Event, EventStatus

router = APIRouter()


@cache(expire=10)
@router.get("/events", response_model=List[Event])
async def get_events(service: EventService = Depends(get_event_service)):
    return await service.list_events()


@router.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: str, service: EventService = Depends(get_event_service)):
    event = await service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/events", response_model=Event)
async def create_event(
    event: CreateEvent, service: EventService = Depends(get_event_service)
):
    try:
        await service.create_event(Event(**event.model_dump()))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    return event


@router.put("/events/{event_id}/status", response_model=Event)
async def update_event_status(
    event_id: str,
    new_status: EventStatus,
    service: EventService = Depends(get_event_service),
    client: httpx.AsyncClient = Depends(get_httpx_client),
):
    try:
        await service.update_event_status(event_id, new_status)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    updated_event = await service.get_event(event_id)
    if updated_event.status in [EventStatus.FINISHED_WIN, EventStatus.FINISHED_LOSE]:
        await client.post(
            url=settings.BET_SERVICE_CALLBACK_URL,
            params={
                "event_id": updated_event.event_id,
                "event_status": updated_event.status.value,
            },
        )
    return updated_event


@router.delete("/events")
async def delete_event(
    event_id: str, service: EventService = Depends(get_event_service)
):
    return await service.delete_event(event_id)
