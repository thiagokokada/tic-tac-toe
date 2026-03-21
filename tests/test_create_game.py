from uuid import UUID, uuid4

from fastapi.testclient import TestClient

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
    game_response = client.post("/games")
    game_id = game_response.json()["game_id"]

    response = client.post(f"/games/{game_id}/moves", json={"x": 1, "y": 1})

    assert response.status_code == 200


def test_make_move_returns_404_for_non_existent_game() -> None:
    response = client.post(f"/games/{uuid4}/moves", json={"x": 1, "y": 1})

    assert response.status_code == 404
