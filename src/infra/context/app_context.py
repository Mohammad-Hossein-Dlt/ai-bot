from typing import ClassVar
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient
from src.infra.schemas.database.redis import RedisClient
from src.infra.schemas.auth.jwt_params import JWTParams
from aiohttp import ClientSession
from openai import OpenAI

class AppContext(type):
    
    platform: ClassVar[str] = None
    db_client: ClassVar[SqlalchemyClient | MongodbClient] = None
    cache_client: ClassVar[RedisClient] = None
    http_client: ClassVar[ClientSession] = None
    gpt_client: ClassVar[OpenAI] = None
    jwt: ClassVar[JWTParams] = None