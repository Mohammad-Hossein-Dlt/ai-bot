from src.domain.enums import AiPlatformType, AiActionType
from pydantic import BaseModel

class CreateCategoryInput(BaseModel):
    parent_id: int | str | None = None
    ai_action_type: AiActionType
    ai_platform_type: AiPlatformType
    slug: str
    name: str
    tokens: int
