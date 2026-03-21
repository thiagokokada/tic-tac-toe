from dataclasses import dataclass, field

from app.domain.exceptions import CellOccupiedError
from app.domain.schemas import (
    BoardData,
    Cell,
    Coordinates,
    GameStatus,
)


def _new_board() -> BoardData:
    return [
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
    ]


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
        assert 0 <= x <= 2 and 0 <= y <= 2, f"Invalid coordinates: x={x}, y={y}"

        if (c := self.data[y][x]) != Cell.NEUTRAL:
            raise CellOccupiedError(x=x, y=y, cell=c)

        self.data[y][x] = cell
        return self.data

    def check_winner(self) -> Cell | None:
        lines = [
            self.data[0],
            self.data[1],
            self.data[2],
            [self.data[0][0], self.data[1][0], self.data[2][0]],
            [self.data[0][1], self.data[1][1], self.data[2][1]],
            [self.data[0][2], self.data[1][2], self.data[2][2]],
            [self.data[0][0], self.data[1][1], self.data[2][2]],
            [self.data[0][2], self.data[1][1], self.data[2][0]],
        ]

        for line in lines:
            first = line[0]
            if first != Cell.NEUTRAL and line[0] == line[1] == line[2]:
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
