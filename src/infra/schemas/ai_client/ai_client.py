from pydantic import BaseModel, ConfigDict
from openai import OpenAI

class AiClient(BaseModel):
    google_ai_client: OpenAI
    open_ai_client: OpenAI

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )