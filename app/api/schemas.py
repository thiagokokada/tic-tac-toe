from datetime import datetime

from pydantic import BaseModel, Field

from app.domain.board import N
from app.domain.schemas import BoardData, Cell, GameStatus


class CreateGameResponse(BaseModel):
    game_id: str
    created_at: datetime


class GameSummary(BaseModel):
    game_id: str
    created_at: datetime
    status: GameStatus


class MoveRequest(BaseModel):
    x: int = Field(ge=0, le=N - 1)
    y: int = Field(ge=0, le=N - 1)


class MoveSummary(BaseModel):
    player: Cell
    x: int
    y: int


class MoveResponse(BaseModel):
    game_id: str
    status: GameStatus
    board: BoardData
    winner: Cell | None = None


class MoveListResponse(BaseModel):
    game_id: str
    moves: list[MoveSummary]


class GameListResponse(BaseModel):
    games: list[GameSummary]
