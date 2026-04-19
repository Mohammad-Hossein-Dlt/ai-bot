from src.domain.enums import AiPlatformType, AiActionType
from pydantic import BaseModel
from typing import TypeAlias, Literal

based_on_const: TypeAlias = Literal[
    "parent-id",
    "child-to-parent",
]

class CategoryFilterInput(BaseModel):
    id: int | str | None = None
    based_on: based_on_const = "parent-id"
    ai_action_type: AiActionType | None = None
    ai_platform_type: AiPlatformType | None = None
