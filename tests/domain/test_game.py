import random

from app.domain.board import Board
from app.domain.game import Game, make_computer_move
from app.domain.schemas import Cell


def test_apply_computer_move_places_o_in_available_position() -> None:
    game = Game(
        board=Board(
            [
                [Cell.X, Cell.NEUTRAL, Cell.O],
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
                [Cell.O, Cell.NEUTRAL, Cell.NEUTRAL],
            ]
        ),
        computer_move_fn=lambda board: make_computer_move(board, rng=random.Random(0)),
    )

    move = game.apply_computer_move()

    assert move in [(1, 0), (0, 1), (2, 1), (1, 2), (2, 2)]
    assert game.board.data[move[1]][move[0]] == Cell.O
    assert game.moves[-1].player == Cell.O
    assert (game.moves[-1].x, game.moves[-1].y) == move


def test_apply_computer_move_returns_none_when_no_moves_are_available() -> None:
    board = Board(
        [
            [Cell.X, Cell.O, Cell.X],
            [Cell.X, Cell.O, Cell.O],
            [Cell.O, Cell.X, Cell.X],
        ]
    )
    game = Game(
        board=board,
        computer_move_fn=lambda board: make_computer_move(board, rng=random.Random(0)),
    )

    move = game.apply_computer_move()

    assert move is None
    assert game.board.data == board.data
    assert game.moves == []
