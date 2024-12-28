from fastapi import FastAPI
from src.api.routers import bet_router

app = FastAPI(
    title="Bet Maker service"
)

app.include_router(bet_router.router, prefix="/api", tags=["Bet"])
