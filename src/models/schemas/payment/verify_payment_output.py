from pydantic import BaseModel

class VerifyPaymentOutput(BaseModel):
    code: str | int
    ref_id: str