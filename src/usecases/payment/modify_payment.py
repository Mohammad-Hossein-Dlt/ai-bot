from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.models.schemas.payment.modify_payment_input import ModifyPaymentInput
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
        payment: ModifyPaymentInput,
    ) -> PaymentModel:
        
        try:
            
            to_modify = PaymentModel()
            
            if payment.payment_id:
                to_modify: PaymentModel = await self.payment_repo.get_by_id(payment.payment_id)
            if payment.user_id:
                to_modify: PaymentModel = await self.payment_repo.get_by_user_id(payment.user_id)
                
            to_modify.status = payment.status
            
            return await self.payment_repo.modify(to_modify)
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 