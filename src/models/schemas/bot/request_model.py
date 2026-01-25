from pydantic import BaseModel

class RequestModel(BaseModel):
    prompts: list[str] = []
    words_number: int = 0
    tones: list[str] = []
