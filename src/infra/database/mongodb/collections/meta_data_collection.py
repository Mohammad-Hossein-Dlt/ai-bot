from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field
from src.domain.schemas.meta_data.meta_data_model import MetaDataModel

class MetaDataCollection(MetaDataModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    channel_id: str
    support_id: str
    bot_id: str
    
    class Settings:
        name = "Meta_Data"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
