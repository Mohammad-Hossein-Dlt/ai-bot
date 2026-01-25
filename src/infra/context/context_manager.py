from .app_context import AppContext
from src.infra.settings.settings import settings
from src.infra.bootstrap.database import init_database_client, terminate_database_client
from src.infra.bootstrap.cache_database import init_cache_client, terminate_cache_client
from src.infra.bootstrap.jwt import init_jwt
from src.infra.bootstrap.gpt_client import init_gpt_client
from aiohttp import ClientSession

class AppContextManager:
        
    @classmethod
    def init_context(cls):        
        AppContext.platform = settings.PLATFORM
        AppContext.gpt_client = init_gpt_client()
        AppContext.jwt = init_jwt()
        
    @classmethod
    async def lazy_init_context(cls):
        
        print("Starting up...")
        
        AppContext.db_client = await init_database_client()
        AppContext.cache_client = await init_cache_client()
        AppContext.http_client = ClientSession()
        
    @classmethod
    async def terminate_context(cls):
        
        print("Shutting down...")
        
        await terminate_database_client(AppContext.db_client)
        await terminate_cache_client(AppContext.cache_client)
        await AppContext.http_client.close()