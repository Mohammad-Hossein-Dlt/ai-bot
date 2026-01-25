from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field
from src.domain.schemas.bot_settings.bot_settings_model import BotSettingsModel

class BotSettingsCollection(BotSettingsModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    enable_bot: bool
    
    class Settings:
        name = "BotSettings"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
