from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field
from src.domain.schemas.discount_code.discount_code_model import DiscountCodeModel
from datetime import datetime

class DiscountCodeCollection(DiscountCodeModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    code: str
    percent: int
    expires_at: datetime
    
    class Settings:
        name = "Discount_Code"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
