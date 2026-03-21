import random
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.domain.board import make_computer_move
from app.domain.schemas import Board, Cell, GameStatus
import app.api.routes.games as games_routes
from app.main import app

from pytest import MonkeyPatch


client = TestClient(app)


def deterministic_make_computer_move(
    board: list[list[Cell]],
) -> tuple[Board, tuple[int, int] | None]:
    return make_computer_move(board, rng=random.Random(0))


def test_create_game_returns_201() -> None:
    response = client.post("/games")

    assert response.status_code == 201

    data = response.json()

    assert set(data.keys()) == {"game_id", "created_at"}

    assert isinstance(data["game_id"], str)
    assert UUID(data["game_id"])

    assert isinstance(data["created_at"], str)


def test_make_move_returns_200(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(games_routes, "make_computer_move", deterministic_make_computer_move)
    game_id = client.post("/games").json()["game_id"]

    response = client.post(f"/games/{game_id}/moves", json={"x": 1, "y": 1})

    assert response.status_code == 200

    data = response.json()

    assert set(data.keys()) == {"game_id", "status", "board", "winner"}
    assert data["game_id"] == game_id
    assert data["status"] == str(GameStatus.IN_PROGRESS)
    assert data["winner"] is None
    assert data["board"] == [
        [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
        [str(Cell.NEUTRAL), str(Cell.X), str(Cell.NEUTRAL)],
        [str(Cell.NEUTRAL), str(Cell.O), str(Cell.NEUTRAL)],
    ]


def test_make_move_in_non_neutral_space_returns_400(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(games_routes, "make_computer_move", deterministic_make_computer_move)
    game_id = client.post("/games").json()["game_id"]

    client.post(f"/games/{game_id}/moves", json={"x": 1, "y": 1})
    response = client.post(f"/games/{game_id}/moves", json={"x": 1, "y": 1})

    assert response.status_code == 400
    assert response.json()["detail"] == "Position x=1, y=1 is already occupied by 'X'"


def test_make_move_returns_404_for_non_existent_game() -> None:
    response = client.post(f"/games/{uuid4()}/moves", json={"x": 1, "y": 1})

    assert response.status_code == 404


def test_make_move_returns_422_for_invalid_move() -> None:
    for x, y in ((-1, 1), (1, -1), (1, 3), (3, 1)):
        response = client.post(f"/games/{uuid4()}/moves", json={"x": x, "y": y})

        assert response.status_code == 422


def test_make_move_returns_player_won_when_x_completes_a_line(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(games_routes, "make_computer_move", deterministic_make_computer_move)
    game_id = client.post("/games").json()["game_id"]

    client.post(f"/games/{game_id}/moves", json={"x": 0, "y": 0})
    client.post(f"/games/{game_id}/moves", json={"x": 1, "y": 0})
    response = client.post(f"/games/{game_id}/moves", json={"x": 2, "y": 0})

    assert response.status_code == 200
    assert response.json()["status"] == str(GameStatus.PLAYER_WON)
    assert response.json()["winner"] == str(Cell.X)
    assert response.json()["board"] == [
        [str(Cell.X), str(Cell.X), str(Cell.X)],
        [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.O)],
        [str(Cell.NEUTRAL), str(Cell.O), str(Cell.NEUTRAL)],
    ]


def test_make_move_returns_400_when_game_is_already_finished(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(games_routes, "make_computer_move", deterministic_make_computer_move)
    game_id = client.post("/games").json()["game_id"]

    client.post(f"/games/{game_id}/moves", json={"x": 0, "y": 0})
    client.post(f"/games/{game_id}/moves", json={"x": 1, "y": 0})
    client.post(f"/games/{game_id}/moves", json={"x": 2, "y": 0})
    response = client.post(f"/games/{game_id}/moves", json={"x": 0, "y": 1})

    assert response.status_code == 400
    assert response.json()["detail"] == "Game is already finished"


def test_list_moves_returns_moves_in_chronological_order(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(games_routes, "make_computer_move", deterministic_make_computer_move)
    game_id = client.post("/games").json()["game_id"]

    client.post(f"/games/{game_id}/moves", json={"x": 1, "y": 1})
    response = client.get(f"/games/{game_id}/moves")

    assert response.status_code == 200
    assert response.json() == {
        "game_id": game_id,
        "moves": [
            {"player": str(Cell.X), "x": 1, "y": 1},
            {"player": str(Cell.O), "x": 1, "y": 2},
        ],
    }
