# Tic-Tac-Toe API

A small FastAPI service that lets a player play tic-tac-toe against the
computer through a REST API.

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

Run linters:

```bash
uv run mypy .
uv run ruff check .
uv run ruff format --check .
```

## API Overview

Available endpoints:

- `POST /games`
- `POST /games/{game_id}/moves`
- `GET /games/{game_id}/moves`
- `GET /games`
- `GET /games/{game_id}/board.txt`

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

Render the current board as plain text:

```bash
curl http://127.0.0.1:8000/games/7a9fbf66-633e-4b17-b42d-3e56bc7a3086/board.txt
```

Example response:

```text
- | - | -
---------
- | X | -
---------
- | O | -
```

## Why ___?

### FastAPI

My initial idea was to use [Flask](https://flask.palletsprojects.com/) since
this is what I am mostly used, but I was curious about
[FastAPI](https://fastapi.tiangolo.com/) for a while. All my recent Python
projects are done with type annotations, so having a fully typed framework was
an interesting choice for this project.

I also like the idea of having `Pydantic` to validate all request/response
schemas, and the fact that I can get documentation generated automatically from
the schemas is a bonus.

### pytest

I much prefer to write tests using `pytest` instead of `unittest`, since they
require less boilerplate.

### uv/ruff

Very fast formatter/linter and dependency manager. This basically replaced the
`black`/`pylint`/`pip`/`Poetry` for most of my recent projects.

### mypy

I am very interested in [ty](https://docs.astral.sh/ty/) from the same creators
of uv/ruff, but it is still in alpha, so I decided to use the good-old
[mypy](https://mypy-lang.org/). Yes, `mypy` is slow, but it doesn't matter too
much in such a small codebase.

I also spent all my [innovation
tokens](https://mcfunley.com/choose-boring-technology) in FastAPI already.

## Notes

- Game state is currently stored in memory.
- Restarting the app clears all games.
- Move coordinates are zero-based.
- The computer move is random in the application.
- Took around 4 hours to implement.

## Assumptions And Trade-Offs

- The player always goes first as `X`.
- The computer always plays as `O`.
- There is no persistent storage.
- Board is 3x3.
- The API is intentionally simple and unauthenticated.
