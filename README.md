# Tic-Tac-Toe API

A small FastAPI service that lets a player play tic-tac-toe against the computer through a REST API.

## Requirements

- Python 3.13+
- `uv`

## Setup

Install dependencies:

```bash
uv sync
```

## Run The App

Start the development server from the project root:

```bash
uv run fastapi dev
```

The app will be available at:

- `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Run Tests

Run the test suite:

```bash
uv run pytest
```

Run only domain tests:

```bash
uv run pytest tests/domain/test_board.py
```

Run only API tests:

```bash
uv run pytest tests/api/test_games.py
```

Run type checks:

```bash
uv run mypy .
```

## API Overview

Available endpoints:

- `POST /games`
- `POST /games/{game_id}/moves`
- `GET /games/{game_id}/moves`
- `GET /games`

The player is always `X` and the computer is always `O`.

## API Examples

Create a new game:

```bash
curl -X POST http://127.0.0.1:8000/games
```

Example response:

```json
{
  "game_id": "7a9fbf66-633e-4b17-b42d-3e56bc7a3086",
  "created_at": "2026-03-21T19:00:00.000000Z"
}
```

Make a move:

```bash
curl -X POST http://127.0.0.1:8000/games/7a9fbf66-633e-4b17-b42d-3e56bc7a3086/moves \
  -H "Content-Type: application/json" \
  -d '{"x": 1, "y": 1}'
```

Example response:

```json
{
  "game_id": "7a9fbf66-633e-4b17-b42d-3e56bc7a3086",
  "status": "in_progress",
  "board": [
    ["-", "-", "-"],
    ["-", "X", "-"],
    ["-", "O", "-"]
  ],
  "winner": null
}
```

List all moves for a game:

```bash
curl http://127.0.0.1:8000/games/7a9fbf66-633e-4b17-b42d-3e56bc7a3086/moves
```

Example response:

```json
{
  "game_id": "7a9fbf66-633e-4b17-b42d-3e56bc7a3086",
  "moves": [
    {"player": "X", "x": 1, "y": 1},
    {"player": "O", "x": 1, "y": 2}
  ]
}
```

List all games:

```bash
curl http://127.0.0.1:8000/games
```

Example response:

```json
{
  "games": [
    {
      "game_id": "7a9fbf66-633e-4b17-b42d-3e56bc7a3086",
      "created_at": "2026-03-21T19:00:00.000000Z",
      "status": "in_progress"
    }
  ]
}
```

## Notes

- Game state is currently stored in memory.
- Restarting the app clears all games.
- Move coordinates are zero-based.
- The computer move is random in the application.

## Assumptions And Trade-Offs

- The player always goes first as `X`.
- The computer always plays as `O`.
- The API is intentionally simple and unauthenticated.
