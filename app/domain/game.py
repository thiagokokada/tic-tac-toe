import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.board import Board
from app.domain.exceptions import GameFinishedError
from app.domain.schemas import (
    Cell,
    ComputerMoveFn,
    Coordinates,
    GameStatus,
)


def computer_random_move(
    available_moves: list[Coordinates],
    rng: random.Random | None = None,
) -> Coordinates | None:
    if not available_moves:
        return None

    if rng is None:
        rng = random.Random()

    x, y = rng.choice(available_moves)
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
    computer_move_fn: ComputerMoveFn = computer_random_move

    def winner(self) -> Cell | None:
        return self.board.check_winner()

    def apply_player_move(self, x: int, y: int) -> None:
        self._apply_move(x=x, y=y, player=Cell.X)

    def apply_computer_move(self) -> None:
        if not self._in_progress():
            return

        move = self.computer_move_fn(self.board.available_moves())
        if move is not None:
            self._apply_move(x=move.x, y=move.y, player=Cell.O)

    def render_board(self) -> str:
        return self.board.render()

    def _update_status(self) -> GameStatus:
        self.status = self.board.check_game_result()
        return self.status

    def _in_progress(self) -> bool:
        return self._update_status() == GameStatus.IN_PROGRESS

    def _apply_move(self, x: int, y: int, player: Cell) -> None:
        if not self._in_progress():
            raise GameFinishedError()
        self.board.apply_move(x=x, y=y, cell=player)
        self.moves.append(Move(player=player, x=x, y=y))
        self._update_status()
