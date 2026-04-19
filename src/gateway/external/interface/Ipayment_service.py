from abc import ABC, abstractmethod
from src.domain.schemas.payment.payment_model import PaymentModel
from src.models.schemas.payment.verify_payment_input import VerifyPaymentInput
from src.models.schemas.payment.verify_payment_output import VerifyPaymentOutput

class IPaymentService(ABC):
    
    @abstractmethod
    async def payment_request(
        payment: PaymentModel,
    ) -> tuple[str, str]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def verify_request(
        to_verify: VerifyPaymentInput,
    ) -> VerifyPaymentOutput:
    
        raise NotImplementedError