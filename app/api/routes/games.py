from datetime import datetime, timezone
from uuid import uuid4

from fastapi import APIRouter, status

from app.api.schemas import CreateGameResponse

router = APIRouter(prefix="/games", tags=["games"])


@router.post("", response_model=CreateGameResponse, status_code=status.HTTP_201_CREATED)
def create_game() -> CreateGameResponse:
    game_id = str(uuid4())
    created_at = datetime.now(timezone.utc)

    return CreateGameResponse(
        game_id=game_id,
        created_at=created_at,
    )
