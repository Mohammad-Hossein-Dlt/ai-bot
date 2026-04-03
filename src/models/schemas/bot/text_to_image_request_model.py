from pydantic import BaseModel

class TextToImageRequestModel(BaseModel):
    ai_platform: str | None = None