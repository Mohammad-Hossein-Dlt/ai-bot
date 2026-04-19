from pydantic import BaseModel

class AddCreditRequestModel(BaseModel):
    tokens: int | None = None
    discount_code: str | None = None