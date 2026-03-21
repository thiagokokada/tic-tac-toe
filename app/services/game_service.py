from collections.abc import Callable
from datetime import datetime, timezone
from uuid import uuid4

from app.domain.board import apply_move, check_game_result, check_winner, new_board
from app.domain.exceptions import GameFinishedError, GameNotFoundError
from app.domain.game import Game, Move
from app.domain.schemas import Board, Cell, GameStatus

type ComputerMoveFn = Callable[[Board], tuple[Board, tuple[int, int] | None]]

games: dict[str, Game] = {}


def create_game() -> Game:
    game_id = str(uuid4())
    created_at = datetime.now(timezone.utc)
    game = Game(
        game_id=game_id,
        created_at=created_at,
        board=new_board(),
    )
    games[game_id] = game
    return game


def list_games() -> list[Game]:
    return sorted(games.values(), key=lambda game: game.created_at)


def get_game(game_id: str) -> Game:
    if game_id not in games:
        raise GameNotFoundError(game_id)
    return games[game_id]


def list_moves(game_id: str) -> list[Move]:
    return get_game(game_id).moves


def make_move(
    game_id: str,
    x: int,
    y: int,
    computer_move_fn: ComputerMoveFn,
) -> tuple[Game, Cell | None]:
    game = get_game(game_id)

    if game.status != GameStatus.IN_PROGRESS:
        raise GameFinishedError()

    board = apply_move(game.board, x=x, y=y, cell=Cell.X)
    game.moves.append(Move(player=Cell.X, x=x, y=y))

    game_status = check_game_result(board)
    winner = check_winner(board)

    if game_status == GameStatus.IN_PROGRESS:
        board, computer_move = computer_move_fn(board)
        if computer_move is not None:
            game.moves.append(Move(player=Cell.O, x=computer_move[0], y=computer_move[1]))
        game_status = check_game_result(board)
        winner = check_winner(board)

    game.board = board
    game.status = game_status
    games[game_id] = game

    return game, winner
