from src.infra.utils.custom_base_model import CustomBaseModel
from src.domain.enums import PlatformEntities
from pydantic import Field, model_validator
from datetime import datetime, timezone
from typing import Self

class AccountModel(CustomBaseModel):
    chat_id: str
    platform: PlatformEntities = Field(default=PlatformEntities.telegram)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        
    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
        
        return self