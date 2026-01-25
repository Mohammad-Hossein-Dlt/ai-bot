from openai import OpenAI
from src.infra.context.app_context import AppContext

def gpt_client_depend() -> OpenAI:
    return AppContext.gpt_client