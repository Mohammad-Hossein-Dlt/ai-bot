from src.infra.settings.settings import settings
from src.infra.database.postgresql.connection import init_postgresql_client, create_tables
from src.infra.database.mongodb.connection import init_mongodb_client
from src.infra.schemas.database.sqlalchemy import SqlalchemyClient
from src.infra.schemas.database.mongodb import MongodbClient

async def postgresql_bootstrap() -> SqlalchemyClient:
    
    sql_client, engine = init_postgresql_client(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        username=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        db_name=settings.POSTGRES_DB
    )
    create_tables(engine)
    
    return SqlalchemyClient(
        client=sql_client,
        engine=engine,
    )

async def mongodb_bootstrap() -> MongodbClient:
    
    mongo_client = await init_mongodb_client(
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        username=settings.MONGO_INITDB_ROOT_USERNAME,
        password=settings.MONGO_INITDB_ROOT_PASSWORD,
        db_name=settings.MONGO_INITDB_DATABASE,
    )
    
    return MongodbClient(
        client=mongo_client,
    )

async def init_database_client() -> SqlalchemyClient | MongodbClient:
    
    if settings.DB_STACK == "postgresql":
        return await postgresql_bootstrap()
    elif settings.DB_STACK == "mongo_db":
        return await mongodb_bootstrap()

async def terminate_database_client(
    context: SqlalchemyClient | MongodbClient | None = None,
):
    
    if not context:
        return
    
    if isinstance(context, SqlalchemyClient):
        context.client.close_all()       
        context.engine.dispose()
        
    if isinstance(context, MongodbClient):
        context.client.close()
