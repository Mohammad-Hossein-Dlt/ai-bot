from src.domain.schemas.payment.payment_model import PaymentModel
from src.domain.enums import PaymentStatus
from beanie import Document, PydanticObjectId
from bson import ObjectId
from pydantic import model_validator, Field

class PaymentCollection(PaymentModel, Document):
    
    id: PydanticObjectId = Field(default_factory=ObjectId)
    user_id: PydanticObjectId
    amount: int
    tokens: int
    authority: str | None
    ref_id: str | None
    status: PaymentStatus = Field(default=PaymentStatus.pending)
    
    class Settings:
        name = "Payment"
        
    @model_validator(mode="before")
    def map_id(cls, values: dict) -> dict:

        if "_id" in values:
            values["id"] = values.pop("_id")
        return values
