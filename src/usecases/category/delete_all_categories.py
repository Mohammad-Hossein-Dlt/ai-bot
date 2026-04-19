from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteAllCategories:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        self.category_repo = category_repo   
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            status = await self.category_repo.delete_all_categories()
            return OperationOutput(id=None, request="delete/all_categories", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")  