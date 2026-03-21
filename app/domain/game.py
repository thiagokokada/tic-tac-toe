import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.board import Board
from app.domain.exceptions import GameFinishedError
from app.domain.schemas import (
    Cell,
    ComputerMoveFn,
    ComputerMoveResult,
    Coordinates,
    GameStatus,
)


def make_computer_move(
    board: Board,
    rng: random.Random | None = None,
) -> ComputerMoveResult:
    moves = board.available_moves()
    if not moves:
        return None

    if rng is None:
        rng = random.Random()

    x, y = rng.choice(moves)
    board.apply_move(x=x, y=y, cell=Cell.O)
    return Coordinates(x, y)


@dataclass(slots=True)
class Move:
    player: Cell
    x: int
    y: int


@dataclass(slots=True)
class Game:
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    board: Board = field(default_factory=Board)
    status: GameStatus = GameStatus.IN_PROGRESS
    moves: list[Move] = field(default_factory=list)
    computer_move_fn: ComputerMoveFn = make_computer_move

    def winner(self) -> Cell | None:
        return self.board.check_winner()

    def update_status(self) -> GameStatus:
        self.status = self.board.check_game_result()
        return self.status

    def ensure_in_progress(self) -> None:
        if self.status != GameStatus.IN_PROGRESS:
            raise GameFinishedError()

    def apply_move(self, x: int, y: int, player: Cell) -> None:
        self.board.apply_move(x=x, y=y, cell=player)
        self.moves.append(Move(player=player, x=x, y=y))
        self.update_status()

    def apply_player_move(self, x: int, y: int) -> None:
        self.apply_move(x=x, y=y, player=Cell.X)

    def apply_computer_move(self) -> tuple[int, int] | None:
        move = self.computer_move_fn(self.board)
        if move is not None:
            self.moves.append(Move(player=Cell.O, x=move.x, y=move.y))
        self.update_status()
        return None if move is None else (move.x, move.y)

    def render_board(self) -> str:
        return self.board.render()
