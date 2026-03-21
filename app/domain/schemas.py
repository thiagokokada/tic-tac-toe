from collections.abc import Callable
from enum import Enum
from typing import TYPE_CHECKING, Final, NamedTuple

if TYPE_CHECKING:
    from app.domain.board import Board


type BoardData = list[list[Cell]]
type ComputerMoveResult = Coordinates | None
type ComputerMoveFn = Callable[[Board], ComputerMoveResult]


class Coordinates(NamedTuple):
    x: int
    y: int


class Cell(Enum):
    NEUTRAL: Final = "-"
    X: Final = "X"
    O: Final = "O"  # noqa: E741

    def __str__(self) -> str:
        return self.value


class GameStatus(Enum):
    IN_PROGRESS: Final = "in_progress"
    PLAYER_WON: Final = "player_won"
    COMPUTER_WON: Final = "computer_won"
    DRAW: Final = "draw"

    def __str__(self) -> str:
        return self.value
