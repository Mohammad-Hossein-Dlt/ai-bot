from pydantic import BaseModel

class UpdateTokenSettingsInput(BaseModel):
    tokens_per_prompt: int | None = None
    unit: int | None = None
    min_tokens: int | None = None
    max_tokens: int | None = None