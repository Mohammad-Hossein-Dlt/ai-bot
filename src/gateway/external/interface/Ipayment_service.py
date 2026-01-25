from abc import ABC, abstractmethod
from src.domain.schemas.payment.payment_model import PaymentModel

class IPaymentService(ABC):
    
    @abstractmethod
    async def payment_request(
        payment: PaymentModel,
    ) -> tuple[str, str]:
    
        raise NotImplementedError