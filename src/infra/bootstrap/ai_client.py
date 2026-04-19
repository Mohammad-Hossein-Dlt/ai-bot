from src.infra.schemas.ai_client.ai_client import AiClient
from src.infra.settings.settings import settings
from openai import OpenAI


def init_open_ai_client() -> OpenAI:
    gpt_client = OpenAI(
        api_key=settings.GPT_TOKEN,
        base_url=settings.GPT_BASE_URL,
    )
    return gpt_client

def init_ai_client() -> AiClient:
    
    return AiClient(
        google_ai_client=init_open_ai_client(),
        open_ai_client=init_open_ai_client(),
    )