from openai import OpenAI
from src.infra.settings.settings import settings


def init_gpt_client() -> OpenAI:
    gpt_client = OpenAI(
        api_key=settings.GPT_TOKEN,
        base_url=settings.GPT_BASE_URL,
    )
    return gpt_client

