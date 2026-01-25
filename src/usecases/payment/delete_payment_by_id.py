from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeletePaymentById:
    
    def __init__(
        self,
        payment_repo: IPaymentRepo,
    ):
        
        self.payment_repo = payment_repo
    
    async def execute(
        self,
        payment_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.payment_repo.delete_by_id(payment_id)
            return OperationOutput(id=payment_id, request="delete/payment", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 