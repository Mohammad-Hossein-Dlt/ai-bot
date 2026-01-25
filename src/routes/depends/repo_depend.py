# from fastapi import Depends
from .depend import inject, Depends
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis
from .db_depend import db_depend
from .cache_depend import cache_depend

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
from src.repo.mongodb.user_mongodb_repo import UserMongodbRepo

@inject
def discount_code_repo_depend(
    db_client: AsyncIOMotorClient | Session = Depends(db_depend)
) -> IDiscountCodeRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return DiscountCodeMongodbRepo()

@inject
def meta_data_repo_depend(
    db_client: AsyncIOMotorClient | Session = Depends(db_depend)
) -> IMetaDataRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return MetaDataMongodbRepo()

@inject
def payment_repo_depend(
    db_client: AsyncIOMotorClient | Session = Depends(db_depend)
) -> IPaymentRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return PaymentMongodbRepo()

@inject
def bot_settings_repo_depend(
    db_client: AsyncIOMotorClient | Session = Depends(db_depend)
) -> IBotSettingsRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return BotSettingsMongodbRepo()

@inject
def token_settings_repo_depend(
    db_client: AsyncIOMotorClient | Session = Depends(db_depend)
) -> ITokenSettingsRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return TokenSettingsMongodbRepo()

@inject
def user_repo_depend(
    db_client: AsyncIOMotorClient | Session = Depends(db_depend)
) -> IUserRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(db_client, AsyncIOMotorClient):
        return UserMongodbRepo()
    
@inject
def cache_repo_depend(
    cache_client: Redis = Depends(cache_depend)
) -> ICacheRepo:
    
    # if isinstance(db_client, Session):
    #     return UserPgRepo(db_client)
    
    if isinstance(cache_client, Redis):
        return RedisCacheRepo(cache_client)