from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.account_model import AccountModel

class UserCollection(UserModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    platform_accounts: list[AccountModel]
    tokens: int = Field(default=0)
    
    class Settings:
        name = "Users"
        indexes = [
            "platform_accounts.chat_id"
        ]
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
