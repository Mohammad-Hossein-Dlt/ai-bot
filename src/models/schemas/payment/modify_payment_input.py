from pydantic import BaseModel
from pydantic import Field
from src.domain.enums import PaymentStatus

class ModifyPaymentInput(BaseModel):
    payment_id: int | str | None = None
    user_id:  int | str | None = None
    status: PaymentStatus = Field(default=PaymentStatus.pending)

