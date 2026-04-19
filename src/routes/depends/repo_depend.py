from .depend import inject, Depends
from sqlalchemy.orm import Session
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from redis import Redis
from .db_depend import db_depend
from .cache_depend import cache_depend
from .bot_platform_depend import bot_platform_depend

from src.infra.context.app_context import AppContext

from src.repo.interface.Icache import ICacheRepo
from src.repo.redis.cache_redis_repo import RedisCacheRepo

from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Iuser_repo import IUserRepo

from src.repo.mongodb.discount_code_mongodb_repo import DiscountCodeMongodbRepo
from src.repo.mongodb.meta_data_mongodb_repo import MetaDataMongodbRepo
from src.repo.mongodb.payment_mongodb_repo import PaymentMongodbRepo
from src.repo.mongodb.bot_settings_mongodb_repo import BotSettingsMongodbRepo
from src.repo.mongodb.token_settings_mongodb_repo import TokenSettingsMongodbRepo
from src.repo.mongodb.category_mongodb_repo import CategoryMongodbRepo
from src.repo.mongodb.user_mongodb_repo import UserMongodbRepo

@inject
def discount_code_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_depend)
) -> IDiscountCodeRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return DiscountCodeMongodbRepo()

@inject
def meta_data_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_depend)
) -> IMetaDataRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return MetaDataMongodbRepo()

@inject
def payment_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_depend)
) -> IPaymentRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return PaymentMongodbRepo()

@inject
def bot_settings_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_depend)
) -> IBotSettingsRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return BotSettingsMongodbRepo()

@inject
def token_settings_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_depend)
) -> ITokenSettingsRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return TokenSettingsMongodbRepo()
    
@inject
def category_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_depend)
) -> ITokenSettingsRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return CategoryMongodbRepo()

@inject
def user_repo_depend(
    db_client: AsyncMongoClient | Session = Depends(db_depend),
    bot_platform: str = Depends(bot_platform_depend),
) -> IUserRepo:
    
    bot_platform = AppContext.bot_platform if AppContext.run_platform == "bot" else None
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncMongoClient):
        return UserMongodbRepo(bot_platform)
    
@inject
def cache_repo_depend(
    cache_client: Redis = Depends(cache_depend)
) -> ICacheRepo:
    
    if isinstance(cache_client, Redis):
        return RedisCacheRepo(cache_client)