from app.domain.exceptions import GameNotFoundError
from app.domain.game import Game, Move
from app.domain.schemas import Cell, ComputerMoveFn, GameStatus

games: dict[str, Game] = {}


def create_game(computer_move_fn: ComputerMoveFn) -> Game:
    game = Game(computer_move_fn=computer_move_fn)
    games[game.id] = game
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
) -> tuple[Game, Cell | None]:
    game = get_game(game_id)

    game.ensure_in_progress()
    game.apply_player_move(x=x, y=y)

    if game.status == GameStatus.IN_PROGRESS:
        game.apply_computer_strategy()

    games[game_id] = game

    return game, game.winner()
