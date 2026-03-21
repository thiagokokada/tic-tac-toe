from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from app.api.schemas import Cell
from app.main import app


client = TestClient(app)


def test_create_game_returns_201() -> None:
    response = client.post("/games")

    assert response.status_code == 201

    data = response.json()

    assert set(data.keys()) == {"game_id", "created_at"}

    assert isinstance(data["game_id"], str)
    assert UUID(data["game_id"])

    assert isinstance(data["created_at"], str)


def test_make_move_returns_200() -> None:
    for x, y, board in (
        (
            0,
            0,
            [
                [str(Cell.X), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
            ],
        ),
        (
            0,
            1,
            [
                [str(Cell.NEUTRAL), str(Cell.X), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
            ],
        ),
        (
            1,
            1,
            [
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.X), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
            ],
        ),
        (
            1,
            0,
            [
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
                [str(Cell.X), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
            ],
        ),
        (
            2,
            2,
            [
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.NEUTRAL)],
                [str(Cell.NEUTRAL), str(Cell.NEUTRAL), str(Cell.X)],
            ],
        ),
    ):
        game_id = client.post("/games").json()["game_id"]

        response = client.post(f"/games/{game_id}/moves", json={"x": x, "y": y})

        assert response.status_code == 200

        data = response.json()

        assert set(data.keys()) == {"game_id", "board"}
        assert data["game_id"] == game_id
        assert data["board"] == board


def test_make_move_returns_404_for_non_existent_game() -> None:
    response = client.post(f"/games/{uuid4()}/moves", json={"x": 1, "y": 1})

    assert response.status_code == 404


def test_make_move_returns_422_for_invalid_move() -> None:
    for x, y in ((-1, 1), (1, -1), (1, 3), (3, 1)):
        response = client.post(f"/games/{uuid4()}/moves", json={"x": x, "y": y})

        assert response.status_code == 422
