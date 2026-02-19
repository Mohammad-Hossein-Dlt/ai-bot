from pydantic import BaseModel

class ProduceContentRequestModel(BaseModel):
    prompts: list[str] = []
    words_number: int = 0
    tones: list[str] = []
