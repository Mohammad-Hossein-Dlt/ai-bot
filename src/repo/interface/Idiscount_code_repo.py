from abc import ABC, abstractmethod
from src.domain.schemas.discount_code.discount_code_model import DiscountCodeModel

class IDiscountCodeRepo(ABC):
        
    @abstractmethod
    async def create(
        new_code: DiscountCodeModel,
    ) -> DiscountCodeModel:

        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        code_id: str,
    ) -> DiscountCodeModel:
    
        raise NotImplementedError
        
    @abstractmethod
    async def get_by_code(
        code: str,
    ) -> DiscountCodeModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_all() -> list[DiscountCodeModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        code: DiscountCodeModel,
    ) -> DiscountCodeModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        code_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_code(
        code: str,
    ) -> bool:
    
        raise NotImplementedError
