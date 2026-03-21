import pytest

from app.domain.board import Board
from app.domain.exceptions import CellOccupiedError
from app.domain.schemas import Cell, GameStatus


def test_new_board_returns_empty_3x3_board() -> None:
    assert Board().data == [
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
    ]


def test_available_moves_returns_all_coordinates_for_empty_board() -> None:
    assert Board().available_moves() == [
        (0, 0),
        (1, 0),
        (2, 0),
        (0, 1),
        (1, 1),
        (2, 1),
        (0, 2),
        (1, 2),
        (2, 2),
    ]


def test_available_moves_omits_occupied_cells() -> None:
    board = Board(
        [
            [Cell.X, Cell.NEUTRAL, Cell.O],
            [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
            [Cell.O, Cell.NEUTRAL, Cell.NEUTRAL],
        ]
    )

    assert board.available_moves() == [
        (1, 0),
        (0, 1),
        (2, 1),
        (1, 2),
        (2, 2),
    ]


def test_apply_move_places_mark_for_all_coordinates() -> None:
    for x, y, expected in (
        (
            0,
            0,
            [
                [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            ],
        ),
        (
            2,
            0,
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            ],
        ),
        (
            0,
            1,
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            ],
        ),
        (
            1,
            1,
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            ],
        ),
        (
            2,
            1,
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            ],
        ),
        (
            1,
            0,
            [
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            ],
        ),
        (
            0,
            2,
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
            ],
        ),
        (
            1,
            2,
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
            ],
        ),
        (
            2,
            2,
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
            ],
        ),
    ):
        board = Board()
        board.apply_move(x, y, Cell.X)
        assert board.data == expected


def test_apply_move_raises_error_for_occupied_cell() -> None:
    for x, y in (
        (0, 0),
        (1, 0),
        (2, 0),
        (0, 1),
        (1, 1),
        (2, 1),
        (0, 2),
        (1, 2),
        (2, 2),
    ):
        board = Board()
        board.apply_move(x, y, Cell.X)

        with pytest.raises(
            CellOccupiedError,
            match=rf"Position x={x}, y={y} is already occupied by 'X'",
        ):
            board.apply_move(x, y, Cell.O)


def test_apply_move_asserts_valid_coordinates() -> None:
    for x, y in ((-1, 1), (1, -1), (1, 3), (3, 1)):
        with pytest.raises(
            AssertionError,
            match=rf"Invalid coordinates: x={x}, y={y}",
        ):
            Board().apply_move(x, y, Cell.X)


def test_check_winner_detects_all_winning_lines() -> None:
    for board in (
        Board(
            [
                [Cell.X, Cell.X, Cell.X],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            ]
        ),
        Board(
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.X, Cell.X, Cell.X],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            ]
        ),
        Board(
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.X, Cell.X, Cell.X],
            ]
        ),
        Board(
            [
                [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
            ]
        ),
        Board(
            [
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
            ]
        ),
        Board(
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
            ]
        ),
        Board(
            [
                [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
            ]
        ),
        Board(
            [
                [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
                [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
                [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
            ]
        ),
    ):
        assert board.check_winner() == Cell.X


def test_check_winner_returns_none_when_there_is_no_winner() -> None:
    board = Board(
        [
            [Cell.X, Cell.O, Cell.NEUTRAL],
            [Cell.NEUTRAL, Cell.X, Cell.O],
            [Cell.O, Cell.NEUTRAL, Cell.NEUTRAL],
        ]
    )

    assert board.check_winner() is None


def test_check_draw_returns_true_for_full_board_without_winner() -> None:
    board = Board(
        [
            [Cell.X, Cell.O, Cell.X],
            [Cell.X, Cell.O, Cell.O],
            [Cell.O, Cell.X, Cell.X],
        ]
    )

    assert board.check_draw() is True


def test_check_draw_returns_false_for_board_with_empty_cells() -> None:
    board = Board(
        [
            [Cell.X, Cell.O, Cell.NEUTRAL],
            [Cell.X, Cell.O, Cell.O],
            [Cell.O, Cell.X, Cell.X],
        ]
    )

    assert board.check_draw() is False


def test_check_game_result_returns_player_won() -> None:
    board = Board(
        [
            [Cell.X, Cell.X, Cell.X],
            [Cell.NEUTRAL, Cell.O, Cell.NEUTRAL],
            [Cell.O, Cell.NEUTRAL, Cell.O],
        ]
    )

    assert board.check_game_result() == GameStatus.PLAYER_WON


def test_check_game_result_returns_computer_won() -> None:
    board = Board(
        [
            [Cell.O, Cell.NEUTRAL, Cell.X],
            [Cell.O, Cell.X, Cell.NEUTRAL],
            [Cell.O, Cell.NEUTRAL, Cell.X],
        ]
    )

    assert board.check_game_result() == GameStatus.COMPUTER_WON


def test_check_game_result_returns_draw() -> None:
    board = Board(
        [
            [Cell.X, Cell.O, Cell.X],
            [Cell.X, Cell.O, Cell.O],
            [Cell.O, Cell.X, Cell.X],
        ]
    )

    assert board.check_game_result() == GameStatus.DRAW


def test_check_game_result_returns_in_progress() -> None:
    board = Board(
        [
            [Cell.X, Cell.O, Cell.NEUTRAL],
            [Cell.NEUTRAL, Cell.X, Cell.O],
            [Cell.O, Cell.NEUTRAL, Cell.NEUTRAL],
        ]
    )

    assert board.check_game_result() == GameStatus.IN_PROGRESS
