from src.infra.settings.settings import settings
from src.infra.database.redis.connection import init_redis_client
from src.infra.schemas.database.redis import RedisClient

async def redis_bootstrap() -> RedisClient:
    
    client = init_redis_client(
        settings.REDIS_HOST,
        settings.REDIS_PORT,
        settings.REDIS_PASSWORD,
    )
    
    return RedisClient(client=client)
    
async def init_cache_client() -> RedisClient:
    
    return await redis_bootstrap()
    
    
async def terminate_cache_client(
    context: RedisClient,
):

    if not context:
        return
    
    if isinstance(context, RedisClient):
        context.client.close()
