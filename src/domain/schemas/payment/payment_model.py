from src.infra.utils.custom_base_model import CustomBaseModel
from src.domain.enums import PaymentStatus
from pydantic import Field, model_validator
from beanie import PydanticObjectId
from datetime import datetime, timezone
from typing import Self

class PaymentModel(CustomBaseModel):
    id: int | PydanticObjectId | None = None
    user_id:  int | PydanticObjectId | None = None
    amount: int | None = None
    tokens: int | None = None
    authority: str | None = None
    ref_id: str | None = None
    status: PaymentStatus = Field(default=PaymentStatus.pending)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
        
    @model_validator(mode='after')
    def validate_values(
        self
    ) -> Self:
        
        if "updated_at" not in self.model_fields_set:
            self.updated_at = self.created_at
        
        return self