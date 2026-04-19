from src.domain.enums import AiPlatformType, AiActionType
from pydantic import BaseModel

class UpdateCategoryInput(BaseModel):
    id: int | str
    parent_id: int | str | None = None
    ai_action_type: AiActionType | None = None
    ai_platform_type: AiPlatformType | None = None
    slug: str | None = None
    name: str | None = None
    tokens: int | None = None
