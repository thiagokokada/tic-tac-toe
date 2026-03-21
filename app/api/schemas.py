from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Cell = Literal["-", "X", "O"]


class CreateGameResponse(BaseModel):
    game_id: str
    created_at: datetime


class MoveRequest(BaseModel):
    x: int = Field(ge=0, le=2)
    y: int = Field(ge=0, le=2)


class MoveResponse(BaseModel):
    game_id: str
    board: list[list[Cell]]
