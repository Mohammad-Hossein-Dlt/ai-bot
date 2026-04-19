from src.infra.context.app_context import AppContext

def bot_platform_depend() -> str:
    platform = AppContext.bot_platform
    return platform