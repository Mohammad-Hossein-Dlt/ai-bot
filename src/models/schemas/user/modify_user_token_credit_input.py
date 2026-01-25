from pydantic import BaseModel

class ModifyUserTokenCreditInput(BaseModel):
    chat_id: str
    value: int