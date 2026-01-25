from pydantic import BaseModel
from src.domain.enums import PlatformEntities

class CreateUserInput(BaseModel):
    chat_id: str
    platform: PlatformEntities