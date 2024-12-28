from decimal import Decimal
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class BetStatus(str, Enum):
    WAIT = "WAIT"
    WIN = "WIN"
    LOSE = "LOSE"


class Bet(BaseModel):
    bet_id: str = Field(default_factory=lambda: uuid4().hex)
    event_id: str
    amount: Decimal = Field(gt=0, decimal_places=2)
    status: BetStatus = BetStatus.WAIT


class CreateBet(BaseModel):
    event_id: str
    amount: Decimal = Field(gt=0, decimal_places=2)
    status: BetStatus = BetStatus.WAIT
