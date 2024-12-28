from typing import List, Optional

from src.domain.bet_model import Bet, BetStatus, CreateBet
from src.domain.bet_repository import BetRepository


class BetService:
    def __init__(self, repository: BetRepository):
        self.repository = repository

    async def get_bet(self, bet_id: str) -> Optional[Bet]:
        return await self.repository.get_bet(bet_id)

    async def list_bets(self) -> List[Bet]:
        return await self.repository.list_bets()

    async def create_bet(self, bet: CreateBet) -> None:
        existing_bet = await self.repository.get_bet(bet.bet_id)
        if existing_bet:
            raise ValueError("Bet with this ID already exists.")
        await self.repository.create_bet(bet)

    async def update_bets_status_by_id(
        self, event_id: str, new_status: BetStatus
    ) -> None:
        bets = await self.repository.get_bets_by_event_id(event_id)
        for bet in bets:
            bet.status = new_status
            await self.repository.update_bet(bet)

    async def delete_bet(self, bet_id: str) -> None:
        return await self.repository.delete_bet(bet_id)
