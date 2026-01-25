from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteMetaData:
    
    def __init__(
        self,
        meta_data_repo: IMetaDataRepo,
    ):
        
        self.meta_data_repo = meta_data_repo
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            status = await self.meta_data_repo.delete()
            return OperationOutput(id=None, request="delete/meta_data", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 