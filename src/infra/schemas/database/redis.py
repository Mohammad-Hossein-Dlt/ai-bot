from .base_client import BaseDatabaseClient
from pydantic import BaseModel, ConfigDict
from redis import Redis

class RedisParams(BaseModel):
    host: str
    port: int
    password: str

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class RedisClient(BaseDatabaseClient, BaseModel):
    client: Redis

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    def get_dependency(self):
        yield self.client
