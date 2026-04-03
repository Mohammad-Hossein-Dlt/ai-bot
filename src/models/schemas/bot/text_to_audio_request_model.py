from pydantic import BaseModel

class TextToAudioRequestModel(BaseModel):
    ai_platform: str | None = None