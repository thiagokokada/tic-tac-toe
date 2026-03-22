import random

import pytest

from app.domain.board import Board
from app.domain.exceptions import GameFinishedError
from app.domain.game import Game, computer_random_move
from app.domain.schemas import Cell


def test_game_defaults_to_empty_in_progress_state() -> None:
    game = Game()

    assert game.status.value == "in_progress"
    assert game.moves == []
    assert game.board.data == [
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
    ]


def test_apply_player_move_updates_board_moves_and_status() -> None:
    game = Game()

    game.apply_player_move(1, 1)

    assert game.board.data == [
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
    ]
    assert len(game.moves) == 1
    assert game.moves[0].player == Cell.X
    assert (game.moves[0].x, game.moves[0].y) == (1, 1)
    assert game.status.value == "in_progress"


def test_move_history_is_kept_in_chronological_order() -> None:
    game = Game(
        computer_move_fn=lambda available_moves: computer_random_move(
            available_moves, rng=random.Random(0)
        )
    )

    game.apply_player_move(1, 1)
    game.apply_computer_move()

    assert [(move.player, move.x, move.y) for move in game.moves] == [
        (Cell.X, 1, 1),
        (Cell.O, 1, 2),
    ]


def test_apply_computer_move_places_o_in_available_position() -> None:
    game = Game(
        board=Board(
            [
                [Cell.X, Cell.NEUTRAL, Cell.O],
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
                [Cell.O, Cell.NEUTRAL, Cell.NEUTRAL],
            ]
        ),
        computer_move_fn=lambda available_moves: computer_random_move(
            available_moves, rng=random.Random(0)
        ),
    )

    game.apply_computer_move()

    assert game.moves[-1].player == Cell.O
    assert (game.moves[-1].x, game.moves[-1].y) in [
        (1, 0),
        (0, 1),
        (2, 1),
        (1, 2),
        (2, 2),
    ]
    assert game.board.data[game.moves[-1].y][game.moves[-1].x] == Cell.O


def test_apply_computer_move_raises_when_no_moves_are_available() -> None:
    board = Board(
        [
            [Cell.X, Cell.O, Cell.X],
            [Cell.X, Cell.O, Cell.O],
            [Cell.O, Cell.X, Cell.X],
        ]
    )
    game = Game(
        board=board,
        computer_move_fn=lambda available_moves: computer_random_move(
            available_moves, rng=random.Random(0)
        ),
    )

    with pytest.raises(GameFinishedError, match="Game is already finished"):
        game.apply_player_move(0, 0)
    assert game.board.data == board.data
    assert game.moves == []


def test_apply_computer_move_returns_none_when_game_is_already_finished() -> None:
    game = Game(
        board=Board(
            [
                [Cell.X, Cell.X, Cell.X],
                [Cell.NEUTRAL, Cell.O, Cell.NEUTRAL],
                [Cell.O, Cell.NEUTRAL, Cell.NEUTRAL],
            ]
        )
    )

    game.apply_computer_move()

    assert game.status.value == "player_won"
    assert game.moves == []
