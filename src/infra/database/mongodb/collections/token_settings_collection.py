from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel

class TokenSettingsCollection(TokenSettingsModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    tokens_per_prompt: int
    unit: int
    min_tokens: int
    max_tokens: int
    
    class Settings:
        name = "Token_Settings"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
