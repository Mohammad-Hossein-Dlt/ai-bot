from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .collections.bot_settings_collection import BotSettingsCollection
from .collections.discount_code_collection import DiscountCodeCollection
from .collections.meta_data_collection import MetaDataCollection
from .collections.payment_collection import PaymentCollection
from .collections.token_settings_collection import TokenSettingsCollection
from .collections.user_collection import UserCollection

async def init_mongodb_client(
    host: str,
    port: int,
    username: str,
    password: str,
    db_name: str
) -> AsyncIOMotorClient:
    
    client = AsyncIOMotorClient(
        host=host,
        port=port,
        username=username,
        password=password
    )
    
    await init_beanie(
        database=client[db_name],
        document_models=[
            BotSettingsCollection,
            DiscountCodeCollection,
            MetaDataCollection,
            PaymentCollection,
            TokenSettingsCollection,
            UserCollection,
        ],
    )
    
    return client