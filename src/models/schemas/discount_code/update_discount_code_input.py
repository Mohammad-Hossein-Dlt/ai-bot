from pydantic import BaseModel
from src.domain.enums import ExpirationType

class UpdateDiscountCodeInput(BaseModel):
    id: int | str | None = None
    code: str | None = None
    percent: str | None = None
    expires_at: int | None = None
    expiration_type: ExpirationType | None = None