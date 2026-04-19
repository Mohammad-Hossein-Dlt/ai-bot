from src.infra.context.app_context import AppContext
from src.infra.schemas.ai_client.ai_client import AiClient

def ai_client_depend() -> AiClient:
    return AppContext.ai_client
