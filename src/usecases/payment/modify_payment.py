from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.models.schemas.payment.payment_input import PaymentInput
from src.domain.schemas.payment.payment_model import PaymentModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ModifyPayment:
    
    def __init__(
        self,
        payment_repo: IPaymentRepo,
    ):
        
        self.payment_repo = payment_repo
    
    async def execute(
        self,
        payment: PaymentInput,
    ) -> PaymentModel:
        
        try:
            to_modify: PaymentModel = PaymentModel.model_validate(payment, from_attributes=True)
            return await self.payment_repo.modify(to_modify)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 