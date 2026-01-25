from abc import ABC, abstractmethod
from src.domain.schemas.payment.payment_model import PaymentModel

class IPaymentRepo(ABC):
        
    @abstractmethod
    async def create(
        payment: PaymentModel,
    ) -> PaymentModel:

        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        payment_id: str,
    ) -> PaymentModel:
    
        raise NotImplementedError
        
    @abstractmethod
    async def get_all_by_user_id(
        user_id: str,
    ) -> list[PaymentModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def modify(
        payment: PaymentModel,
    ) -> PaymentModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        payment_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_user_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError