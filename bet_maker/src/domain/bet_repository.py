from abc import ABC, abstractmethod
from typing import List

from src.domain.bet_model import Bet


class BetRepository(ABC):
    @abstractmethod
    async def get_bet(self, bet_id: str) -> Bet:
        pass

    @abstractmethod
    async def list_bets(self) -> List[Bet]:
        pass

    @abstractmethod
    async def create_bet(self, bet: Bet) -> None:
        pass

    @abstractmethod
    async def update_bet(self, bet: Bet) -> None:
        pass

    @abstractmethod
    async def delete_bet(self, bet_id: str) -> None:
        pass
