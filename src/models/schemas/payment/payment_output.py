from pydantic import BaseModel

class PaymentOutput(BaseModel):
    payment_id: int | str
    payment_link: str