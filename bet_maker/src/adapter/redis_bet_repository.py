import json
from typing import List, Optional
from src.domain.bet_model import Bet
from src.domain.bet_repository import BetRepository
from redis.asyncio import Redis


class RedisBetRepository(BetRepository):
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    async def get_bet(self, bet_id: str) -> Optional[Bet]:
        key = f"bet:{bet_id}"
        bet_data = await self.redis.get(key)
        if bet_data:
            bet_dict = json.loads(bet_data)
            return Bet(**bet_dict)
        return None

    async def list_bets(self) -> List[Bet]:
        pattern = "bet:*"
        cursor = 0
        bets = []
        while True:
            cursor, keys = await self.redis.scan(
                cursor=cursor, match=pattern, count=100
            )
            if keys:
                async with self.redis.pipeline() as pipe:
                    for key in keys:
                        pipe.get(key)
                    bets_data = await pipe.execute()
                for bet_data in bets_data:
                    if bet_data:
                        bet_dict = json.loads(bet_data)
                        bets.append(Bet(**bet_dict))
            if cursor == 0:
                break
        return bets

    async def create_bet(self, bet: Bet) -> None:
        key = f"bet:{bet.bet_id}"
        bet_json = bet.model_dump_json()
        await self.redis.set(key, bet_json)
        event_key = f"event_bets:{bet.event_id}"
        await self.redis.sadd(event_key, key)

    async def update_bet(self, bet: Bet) -> None:
        key = f"bet:{bet.bet_id}"
        exists = await self.redis.exists(key)
        if exists:
            bet_json = bet.model_dump_json()
            await self.redis.set(key, bet_json)

    async def delete_bet(self, bet_id: str) -> None:
        key = f"bet:{bet_id}"
        return await self.redis.delete(key)

    async def get_bets_by_event_id(self, event_id: str) -> List[Bet]:
        event_key = f"event_bets:{event_id}"
        bet_keys = await self.redis.smembers(event_key)
        bets = []
        if bet_keys:
            async with self.redis.pipeline() as pipe:
                for key in bet_keys:
                    pipe.get(key)
                bets_data = await pipe.execute()
            for bet_data in bets_data:
                if bet_data:
                    bet_dict = json.loads(bet_data)
                    bets.append(Bet(**bet_dict))
        return bets
