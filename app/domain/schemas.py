from enum import Enum
from typing import Final


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
