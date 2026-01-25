from pydantic import BaseModel

class CreateTokenSettingsInput(BaseModel):
    tokens_per_prompt: int
    unit: int
    min_tokens: int
    max_tokens: int