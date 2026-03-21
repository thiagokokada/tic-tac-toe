from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.schemas import Board, Cell, GameStatus


class CreateGameResponse(BaseModel):
    game_id: str
    created_at: datetime


class MoveRequest(BaseModel):
    x: int = Field(ge=0, le=2)
    y: int = Field(ge=0, le=2)


class MoveResponse(BaseModel):
    game_id: str
    status: GameStatus
    board: Board
    winner: Cell | None = None
