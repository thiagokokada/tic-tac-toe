from dataclasses import dataclass, field
from datetime import datetime

from app.domain.schemas import Board, Cell, GameStatus


@dataclass(slots=True)
class Move:
    player: Cell
    x: int
    y: int


@dataclass(slots=True)
class Game:
    game_id: str
    created_at: datetime
    board: Board
    status: GameStatus = GameStatus.IN_PROGRESS
    moves: list[Move] = field(default_factory=list)
