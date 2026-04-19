from pydantic import BaseModel

class CreatePaymentInput(BaseModel):
    chat_id: str
    amount: int
    tokens: int