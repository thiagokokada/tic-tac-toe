from dataclasses import dataclass, field
from typing import Final

from app.domain.exceptions import CellOccupiedError
from app.domain.schemas import (
    BoardData,
    Cell,
    Coordinates,
    GameStatus,
)

N: Final = 3


def _new_board() -> BoardData:
    return [[Cell.NEUTRAL for _x in range(N)] for _y in range(N)]


@dataclass(slots=True)
class Board:
    data: BoardData = field(default_factory=_new_board)

    def available_moves(self) -> list[Coordinates]:
        return [
            Coordinates(x=x, y=y)
            for y, row in enumerate(self.data)
            for x, cell in enumerate(row)
            if cell == Cell.NEUTRAL
        ]

    def apply_move(self, x: int, y: int, cell: Cell) -> BoardData:
        assert 0 <= x <= N - 1 and 0 <= y <= N - 1, f"Invalid coordinates: x={x}, y={y}"

        if (c := self.data[y][x]) != Cell.NEUTRAL:
            raise CellOccupiedError(x=x, y=y, cell=c)

        self.data[y][x] = cell
        return self.data

    def check_winner(self) -> Cell | None:
        lines = []

        # rows
        lines.extend(self.data)

        # columns
        lines.extend([self.data[y][x] for y in range(N)] for x in range(N))

        # main diagonal
        lines.append([self.data[i][i] for i in range(N)])

        # anti diagonal
        lines.append([self.data[i][N - 1 - i] for i in range(N)])

        for line in lines:
            first = line[0]
            if first is not Cell.NEUTRAL and all(cell == first for cell in line):
                return first

        return None

    def check_draw(self) -> bool:
        return all(cell != Cell.NEUTRAL for row in self.data for cell in row)

    def check_game_result(self) -> GameStatus:
        winner = self.check_winner()

        if winner == Cell.X:
            return GameStatus.PLAYER_WON
        if winner == Cell.O:
            return GameStatus.COMPUTER_WON
        if self.check_draw():
            return GameStatus.DRAW

        return GameStatus.IN_PROGRESS

    def render(self) -> str:
        return "\n---------\n".join(
            " | ".join(str(cell) for cell in row) for row in self.data
        )
