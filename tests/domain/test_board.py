import pytest

from app.domain.board import apply_move, check_draw, check_winner, new_board
from app.domain.exceptions import CellOccupiedError
from app.domain.schemas import Cell


def test_new_board_returns_empty_3x3_board() -> None:
    assert new_board() == [
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
    ]


def test_apply_move_places_mark_for_all_coordinates() -> None:
    for x, y, board in (
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
        assert apply_move(new_board(), x, y, Cell.X) == board


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
        board = apply_move(new_board(), x, y, Cell.X)

        with pytest.raises(
            CellOccupiedError,
            match=rf"Position x={x}, y={y} is already occupied by 'X'",
        ):
            apply_move(board, x, y, Cell.O)


def test_check_winner_detects_all_winning_lines() -> None:
    for board in (
        [
            [Cell.X, Cell.X, Cell.X],
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        ],
        [
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            [Cell.X, Cell.X, Cell.X],
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        ],
        [
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
            [Cell.X, Cell.X, Cell.X],
        ],
        [
            [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
            [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
            [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
        ],
        [
            [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
            [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
            [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
        ],
        [
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
        ],
        [
            [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
            [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
        ],
        [
            [Cell.NEUTRAL, Cell.NEUTRAL, Cell.X],
            [Cell.NEUTRAL, Cell.X, Cell.NEUTRAL],
            [Cell.X, Cell.NEUTRAL, Cell.NEUTRAL],
        ],
    ):
        assert check_winner(board) == Cell.X


def test_check_winner_returns_none_when_there_is_no_winner() -> None:
    board = [
        [Cell.X, Cell.O, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.X, Cell.O],
        [Cell.O, Cell.NEUTRAL, Cell.NEUTRAL],
    ]

    assert check_winner(board) is None


def test_check_draw_returns_true_for_full_board_without_winner() -> None:
    board = [
        [Cell.X, Cell.O, Cell.X],
        [Cell.X, Cell.O, Cell.O],
        [Cell.O, Cell.X, Cell.X],
    ]

    assert check_draw(board) is True


def test_check_draw_returns_false_for_board_with_empty_cells() -> None:
    board = [
        [Cell.X, Cell.O, Cell.NEUTRAL],
        [Cell.X, Cell.O, Cell.O],
        [Cell.O, Cell.X, Cell.X],
    ]

    assert check_draw(board) is False
