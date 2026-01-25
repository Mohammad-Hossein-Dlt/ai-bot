from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from motor.motor_asyncio import AsyncIOMotorClient

class BaseDatabaseClient(ABC):
    
    @abstractmethod
    def get_dependency(self) -> Session | AsyncIOMotorClient:
        raise NotImplementedError