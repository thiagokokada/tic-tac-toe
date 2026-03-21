from datetime import datetime

from pydantic import BaseModel


class CreateGameResponse(BaseModel):
    game_id: str
    created_at: datetime
