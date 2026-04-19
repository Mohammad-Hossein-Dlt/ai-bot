from pydantic import BaseModel

class ContentCreationRequestModel(BaseModel):
    ai_platform: str | None = None
    ai_model_id: str | None = None
    prompts: list[str] = []
    words_number: int = 0
    tones: list[str] = []
