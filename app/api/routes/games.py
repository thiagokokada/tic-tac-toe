from fastapi import APIRouter, HTTPException, status

from app.api.schemas import (
    CreateGameResponse,
    GameListResponse,
    GameSummary,
    MoveListResponse,
    MoveRequest,
    MoveResponse,
    MoveSummary,
)
from app.domain.board import make_computer_move
from app.domain.exceptions import GameError, GameFinishedError, GameNotFoundError
from app.services import game_service

router = APIRouter(prefix="/games", tags=["games"])
games = game_service.games


@router.post("", response_model=CreateGameResponse, status_code=status.HTTP_201_CREATED)
def create_game() -> CreateGameResponse:
    game = game_service.create_game()

    return CreateGameResponse(
        game_id=game.game_id,
        created_at=game.created_at,
    )


@router.get(
    "",
    response_model=GameListResponse,
    status_code=status.HTTP_200_OK,
)
def list_games() -> GameListResponse:
    return GameListResponse(
        games=[
            GameSummary(
                game_id=game.game_id,
                created_at=game.created_at,
                status=game.status,
            )
            for game in game_service.list_games()
        ],
    )


@router.post(
    "/{game_id}/moves",
    response_model=MoveResponse,
    status_code=status.HTTP_200_OK,
)
def make_move(game_id: str, move: MoveRequest) -> MoveResponse:
    try:
        game, winner = game_service.make_move(
            game_id=game_id,
            x=move.x,
            y=move.y,
            computer_move_fn=make_computer_move,
        )
    except GameNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )
    except GameFinishedError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is already finished",
        )
    except GameError as ex:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ex),
        )

    return MoveResponse(
        game_id=game.game_id,
        status=game.status,
        board=game.board,
        winner=winner,
    )


@router.get(
    "/{game_id}/moves",
    response_model=MoveListResponse,
    status_code=status.HTTP_200_OK,
)
def list_moves(game_id: str) -> MoveListResponse:
    try:
        game = game_service.get_game(game_id)
    except GameNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    return MoveListResponse(
        game_id=game.game_id,
        moves=[
            MoveSummary(player=move.player, x=move.x, y=move.y)
            for move in game.moves
        ],
    )
