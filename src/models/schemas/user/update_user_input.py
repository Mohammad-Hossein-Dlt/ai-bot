from pydantic import BaseModel
from src.domain.enums import PlatformEntities

class UpdateUserInput(BaseModel):
    user_id: int | str | None = None
    chat_id: str | None = None
    bot_platform: PlatformEntities | None = None