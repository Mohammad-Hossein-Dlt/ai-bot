from pydantic import BaseModel

class PaymentInput(BaseModel):
    chat_id: str
    amount: int
    tokens: int