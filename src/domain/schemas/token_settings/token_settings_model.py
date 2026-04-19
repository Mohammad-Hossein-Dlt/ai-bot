from src.infra.utils.custom_base_model import CustomBaseModel
from pydantic import Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from typing import Self

class TokenSettingsModel(CustomBaseModel):

    id: int | PydanticObjectId | None = None
    tokens_per_prompt: int | None = None
    unit: int | None = None
    min_tokens: int | None = None
    max_tokens: int | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        
    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
        
        return self