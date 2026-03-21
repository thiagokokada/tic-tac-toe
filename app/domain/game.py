from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
import random

from app.domain.board import (
    apply_move,
    available_moves,
    check_game_result,
    check_winner,
    make_computer_move,
    render_board,
)
from app.domain.exceptions import GameFinishedError
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
    computer_move_fn: Callable[[Board], tuple[Board, tuple[int, int] | None]] = make_computer_move

    def available_moves(self) -> list[tuple[int, int]]:
        return available_moves(self.board)

    def winner(self) -> Cell | None:
        return check_winner(self.board)

    def update_status(self) -> GameStatus:
        self.status = check_game_result(self.board)
        return self.status

    def ensure_in_progress(self) -> None:
        if self.status != GameStatus.IN_PROGRESS:
            raise GameFinishedError()

    def apply_move(self, x: int, y: int, player: Cell) -> None:
        self.board = apply_move(self.board, x=x, y=y, cell=player)
        self.moves.append(Move(player=player, x=x, y=y))
        self.update_status()

    def apply_player_move(self, x: int, y: int) -> None:
        self.apply_move(x=x, y=y, player=Cell.X)

    def apply_computer_move(
        self,
        rng: random.Random | None = None,
    ) -> tuple[int, int] | None:
        self.board, move = make_computer_move(self.board, rng=rng)
        if move is not None:
            self.moves.append(Move(player=Cell.O, x=move[0], y=move[1]))
        self.update_status()
        return move

    def apply_computer_strategy(self) -> tuple[int, int] | None:
        self.board, move = self.computer_move_fn(self.board)
        if move is not None:
            self.moves.append(Move(player=Cell.O, x=move[0], y=move[1]))
        self.update_status()
        return move

    def render_board(self) -> str:
        return render_board(self.board)
