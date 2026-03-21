from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.api.schemas import (
    CreateGameResponse,
    MoveListResponse,
    MoveRequest,
    MoveResponse,
    MoveSummary,
)
from app.domain.board import (
    apply_move,
    check_game_result,
    check_winner,
    make_computer_move,
    new_board,
)
from app.domain.exceptions import GameError
from app.domain.game import Game, Move
from app.domain.schemas import Cell, GameStatus

router = APIRouter(prefix="/games", tags=["games"])
games: dict[str, Game] = {}


@router.post("", response_model=CreateGameResponse, status_code=status.HTTP_201_CREATED)
def create_game() -> CreateGameResponse:
    game_id = str(uuid4())
    created_at = datetime.now(timezone.utc)
    games[game_id] = Game(
        game_id=game_id,
        created_at=created_at,
        board=new_board(),
    )

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

    if game.status != GameStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is already finished",
        )

    try:
        board = apply_move(game.board, x=move.x, y=move.y, cell=Cell.X)
    except GameError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )
    game.moves.append(Move(player=Cell.X, x=move.x, y=move.y))

    game_status = check_game_result(board)
    winner = check_winner(board)

    if game_status == GameStatus.IN_PROGRESS:
        board, computer_move = make_computer_move(board)
        if computer_move is not None:
            game.moves.append(Move(player=Cell.O, x=computer_move[0], y=computer_move[1]))
        game_status = check_game_result(board)
        winner = check_winner(board)

    game.board = board
    game.status = game_status
    games[game_id] = game

    return MoveResponse(
        game_id=game.game_id,
        status=game_status,
        board=board,
        winner=winner,
    )


@router.get(
    "/{game_id}/moves",
    response_model=MoveListResponse,
    status_code=status.HTTP_200_OK,
)
def list_moves(game_id: str) -> MoveListResponse:
    if game_id not in games:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    game = games[game_id]

    return MoveListResponse(
        game_id=game.game_id,
        moves=[
            MoveSummary(player=move.player, x=move.x, y=move.y)
            for move in game.moves
        ],
    )
