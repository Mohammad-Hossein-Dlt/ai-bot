from typing import ClassVar
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient
from src.infra.schemas.database.redis import RedisClient
from src.infra.schemas.auth.jwt_params import JWTParams
from aiohttp import ClientSession
from src.infra.schemas.ai_client.ai_client import AiClient

class AppContext(type):
    
    run_platform: ClassVar[str] = None
    bot_platform: ClassVar[str] = None
    zarinpal_merchant_id: ClassVar[str] = None
    db_client: ClassVar[SqlalchemyClient | MongodbClient] = None
    cache_client: ClassVar[RedisClient] = None
    http_client: ClassVar[ClientSession] = None
    ai_client: ClassVar[AiClient] = None
    jwt: ClassVar[JWTParams] = None