from pydantic import BaseModel

class SuccessPaymentOutput(BaseModel):
    tokens: str | int
    amount: str | int
    code: str | int
    ref_id: str