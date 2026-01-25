from .base_client import BaseDatabaseClient
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Engine
from sqlalchemy.orm import sessionmaker, Session

class SqlalchemyParams(BaseModel):
    host: str
    port: int
    username: str
    password: str
    db_name: str
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class SqlalchemyClient(BaseDatabaseClient, BaseModel):
    engine: Engine
    client: sessionmaker

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
    
    def get_dependency(self):
        session: Session = self.client()
        try:
            yield session
        finally:
            session.close()