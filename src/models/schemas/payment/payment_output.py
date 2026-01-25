from pydantic import BaseModel

class PaymentOutput(BaseModel):
    payment_id: str
    payment_link: str