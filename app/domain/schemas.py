from datetime import datetime
from enum import Enum
from typing import Final

from pydantic import BaseModel, Field


class Cell(Enum):
    NEUTRAL: Final = "-"
    X: Final = "X"
    O: Final = "O"  # noqa: E741

    def __str__(self) -> str:
        return self.value

type Board = list[list[Cell]]


class GameStatus(Enum):
    IN_PROGRESS: Final = "in_progress"
    PLAYER_WON: Final = "player_won"

    def __str__(self) -> str:
        return self.value


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
