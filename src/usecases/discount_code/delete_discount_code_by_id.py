from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteDiscountCodeById:
    
    def __init__(
        self,
        discount_code_repo: IDiscountCodeRepo,
    ):
        
        self.discount_code_repo = discount_code_repo
    
    async def execute(
        self,
        code_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.discount_code_repo.delete_by_id(code_id)
            return OperationOutput(id=code_id, request="delete/discount_code", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 