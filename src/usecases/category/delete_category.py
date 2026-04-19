from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        self.category_repo = category_repo   
    
    async def execute(
        self,
        category_id: str,
    ) -> OperationOutput:
        
        try:
            status = await self.category_repo.delete_category(category_id)
            return OperationOutput(id=category_id, request="delete/category", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  