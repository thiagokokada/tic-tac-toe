from app.domain.exceptions import CellOccupiedError
from app.domain.schemas import Board, Cell


def new_board() -> Board:
    return [
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
    ]


def apply_move(board: Board, x: int, y: int, cell: Cell) -> Board:
    if (c := board[y][x]) != Cell.NEUTRAL:
        raise CellOccupiedError(x=x, y=y, cell=c)

    board[y][x] = cell
    return board
