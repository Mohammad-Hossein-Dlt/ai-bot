from src.infra.context.app_context import AppContext

def cache_depend():
    client = AppContext.cache_client
    yield from client.get_dependency()