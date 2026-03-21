from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.api.schemas import Board, Cell, CreateGameResponse, MoveRequest, MoveResponse

router = APIRouter(prefix="/games", tags=["games"])
games: dict[str, dict] = {}


@router.post("", response_model=CreateGameResponse, status_code=status.HTTP_201_CREATED)
def create_game() -> CreateGameResponse:
    game_id = str(uuid4())
    created_at = datetime.now(timezone.utc)
    games[game_id] = {
        "game_id": game_id,
        "created_at": created_at,
        "board": _new_board(),
    }

    return CreateGameResponse(
        game_id=game_id,
        created_at=created_at,
    )


@router.post(
    "/{game_id}/moves", response_model=MoveResponse, status_code=status.HTTP_200_OK
)
def make_move(game_id: str, move: MoveRequest) -> MoveResponse:
    if game_id in games:
        game = games[game_id]
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found",
        )

    return MoveResponse(
        game_id=game["game_id"],
        board=_apply_move(game["board"], x=move.x, y=move.y, cell=Cell.X),
    )


def _new_board() -> Board:
    return [
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
        [Cell.NEUTRAL, Cell.NEUTRAL, Cell.NEUTRAL],
    ]


def _apply_move(board: Board, x: int, y: int, cell: Cell) -> Board:
    if (c := board[x][y]) != Cell.NEUTRAL:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Position x={x}, y={y} is already occupied by '{c}'",
        )
    board[x][y] = cell
    return board
