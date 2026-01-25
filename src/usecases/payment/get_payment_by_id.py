from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.domain.schemas.payment.payment_model import PaymentModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetPaymentById:
    
    def __init__(
        self,
        payment_repo: IPaymentRepo,
    ):
        
        self.payment_repo = payment_repo
    
    async def execute(
        self,
        payment_id: str,
    ) -> PaymentModel:
        
        try:
            return await self.payment_repo.get_by_id(payment_id)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 