from app.domain.exceptions import CellOccupiedError
from app.domain.schemas import Board, Cell, GameStatus


def new_board() -> Board:
    return [
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
    ]


def available_moves(board: Board) -> list[tuple[int, int]]:
    return [
        (x, y)
        for y, row in enumerate(board)
        for x, cell in enumerate(row)
        if cell == Cell.NEUTRAL
    ]


def apply_move(board: Board, x: int, y: int, cell: Cell) -> Board:
    if (c := board[y][x]) != Cell.NEUTRAL:
        raise CellOccupiedError(x=x, y=y, cell=c)

    board[y][x] = cell
    return board


def check_winner(board: Board) -> Cell | None:
    lines = [
        board[0],
        board[1],
        board[2],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]

    for line in lines:
        first = line[0]
        if first != Cell.NEUTRAL and line[0] == line[1] == line[2]:
            return first

    return None


def check_draw(board: Board) -> bool:
    return all(cell != Cell.NEUTRAL for row in board for cell in row)


def check_game_result(board: Board) -> GameStatus:
    winner = check_winner(board)

    if winner == Cell.X:
        return GameStatus.PLAYER_WON
    if winner == Cell.O:
        return GameStatus.COMPUTER_WON
    if check_draw(board):
        return GameStatus.DRAW

    return GameStatus.IN_PROGRESS
