from src.domain.schemas.category.category_model import CategoryModel
from src.domain.enums import AiActionType, AiPlatformType
from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import Field, model_validator

class CategoryCollection(CategoryModel, Document):

    id: PydanticObjectId = Field(default_factory=ObjectId)
    parent_id: PydanticObjectId | None = None
    ai_action_type: AiActionType
    ai_platform_type: AiPlatformType
    slug: str
    name: str
    tokens: int
    
    class Settings:
        name = "Categories"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
