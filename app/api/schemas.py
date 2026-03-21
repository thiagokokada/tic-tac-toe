from datetime import datetime
from typing import Final, Literal

from pydantic import BaseModel, Field

NEUTRAL: Final = "-"
X: Final = "X"
O: Final = "O"

type Cell = Literal[NEUTRAL, X, O]
type Board = list[list[Cell]]


class CreateGameResponse(BaseModel):
    game_id: str
    created_at: datetime


class MoveRequest(BaseModel):
    x: int = Field(ge=0, le=2)
    y: int = Field(ge=0, le=2)


class MoveResponse(BaseModel):
    game_id: str
    board: list[list[Cell]]
