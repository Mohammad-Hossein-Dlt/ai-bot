from pydantic import BaseModel

class TextToAudioRequestModel(BaseModel):
    ai_platform: str | None = None
    ai_model_id: str | None = None