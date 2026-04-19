from src.infra.utils.custom_base_model import CustomBaseModel
from .account_model import AccountModel
from pydantic import Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from typing import Self

class UserModel(CustomBaseModel):
    
    id: int | PydanticObjectId | None = None
    platform_accounts: list[AccountModel]
    tokens: int = Field(default=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        
    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
        
        return self