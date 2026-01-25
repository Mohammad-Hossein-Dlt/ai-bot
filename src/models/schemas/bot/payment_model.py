from pydantic import BaseModel


class PaymentModel(BaseModel):
    section: str
    step: int
    user_id: str
    payment_id: str
    amount: int
    tokens: int
