from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.api.schemas import (
    CreateGameResponse,
    MoveRequest,
    MoveResponse,
)
from app.domain.board import apply_move, check_winner, new_board
from app.domain.exceptions import GameError
from app.domain.schemas import Cell, GameStatus

router = APIRouter(prefix="/games", tags=["games"])
games: dict[str, dict] = {}


@router.post("", response_model=CreateGameResponse, status_code=status.HTTP_201_CREATED)
def create_game() -> CreateGameResponse:
    game_id = str(uuid4())
    created_at = datetime.now(timezone.utc)
    games[game_id] = {
        "game_id": game_id,
        "created_at": created_at,
        "board": new_board(),
        "status": GameStatus.IN_PROGRESS,
    }

    return CreateGameResponse(
        game_id=game_id,
        created_at=created_at,
    )


@router.post(
    "/{game_id}/moves",
    response_model=MoveResponse,
    status_code=status.HTTP_200_OK,
)
def make_move(game_id: str, move: MoveRequest) -> MoveResponse:
    if game_id in games:
        game = games[game_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    if game["status"] != GameStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is already finished",
        )

    try:
        board = apply_move(game["board"], x=move.x, y=move.y, cell=Cell.X)
    except GameError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )

    winner = check_winner(board)
    game_status = GameStatus.PLAYER_WON if winner == Cell.X else GameStatus.IN_PROGRESS

    game["board"] = board
    game["status"] = game_status
    games[game_id] = game

    return MoveResponse(
        game_id=game["game_id"],
        status=game_status,
        board=board,
        winner=winner,
    )
