from pydantic import BaseModel

class VerifyPaymentInput(BaseModel):
    amount: str | int
    authority: str