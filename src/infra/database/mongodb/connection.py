from pymongo.asynchronous.database import AsyncDatabase
from pymongo.asynchronous.mongo_client import AsyncMongoClient
from beanie import init_beanie
from .collections.bot_settings_collection import BotSettingsCollection
from .collections.discount_code_collection import DiscountCodeCollection
from .collections.meta_data_collection import MetaDataCollection
from .collections.payment_collection import PaymentCollection
from .collections.token_settings_collection import TokenSettingsCollection
from .collections.category_collection import CategoryCollection
from .collections.user_collection import UserCollection

async def init_mongodb_client(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str
) -> AsyncMongoClient:
    
    client = AsyncMongoClient(
        host=host,
        port=port,
        username=username,
        password=password,
    )
    
    database = AsyncDatabase(
        client=client,
        name=db_name,
    )
    
    await init_beanie(
        database=database,
        document_models=[
            BotSettingsCollection,
            DiscountCodeCollection,
            MetaDataCollection,
            PaymentCollection,
            TokenSettingsCollection,
            CategoryCollection,
            UserCollection,
        ],
    )
    
    return client