from pydantic import BaseModel
from src.domain.enums import ExpirationType

class CreateDiscountCodeInput(BaseModel):
    code: str
    percent: str
    expires_at: int
    expiration_type: ExpirationType