from .base_client import BaseDatabaseClient
from pydantic import BaseModel, ConfigDict
from pymongo.asynchronous.mongo_client import AsyncMongoClient

class MongodbParams(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db_name: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class MongodbClient(BaseDatabaseClient, BaseModel):
    client: AsyncMongoClient

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def get_dependency(self):
        yield self.client
