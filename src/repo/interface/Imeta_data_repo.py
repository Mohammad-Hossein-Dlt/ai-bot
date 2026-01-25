from abc import ABC, abstractmethod
from src.domain.schemas.meta_data.meta_data_model import MetaDataModel

class IMetaDataRepo(ABC):
        
    @abstractmethod
    async def create(
        meta_data: MetaDataModel,
    ) -> MetaDataModel:

        raise NotImplementedError
    
    @abstractmethod
    async def get() -> MetaDataModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        meta_data: MetaDataModel,
    ) -> MetaDataModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete() -> bool:
    
        raise NotImplementedError
