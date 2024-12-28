from typing import List

import httpx
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from src.api.deps import get_bet_service, get_httpx_client
from src.application.bet import BetService
from src.core.config import settings
from src.domain.bet_model import Bet, BetStatus, CreateBet

router = APIRouter()


@router.get("/events")
async def get_events(client: httpx.AsyncClient = Depends(get_httpx_client)):
    response = await client.get(settings.EVENT_SERVICE_URL)
    return response.json()


@router.get("/bets", response_model=List[Bet])
async def get_bets(service: BetService = Depends(get_bet_service)):
    return await service.list_bets()


@router.post("/bets", response_model=Bet)
async def create_bet(bet: CreateBet, service: BetService = Depends(get_bet_service)):
    try:
        await service.create_bet(Bet(**bet.model_dump()))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    return bet


@router.post("/callback_event_status_updated")
async def send_data(
    event_id: str,
    event_status: str,
    background_tasks: BackgroundTasks,
    service: BetService = Depends(get_bet_service),
):
    match event_status:
        case "FINISHED_WIN":
            bet_status = BetStatus.WIN
        case "FINISHED_LOSE":
            bet_status = BetStatus.LOSE
        case default:
            return {"message": "error"}
    background_tasks.add_task(service.update_bets_status_by_id, event_id, bet_status)
    return {"message": "updated"}
