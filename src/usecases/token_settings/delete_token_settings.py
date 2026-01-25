from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteTokenSettings:
    
    def __init__(
        self,
        token_settings_repo: ITokenSettingsRepo,
    ):
        
        self.token_settings_repo = token_settings_repo
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            status = await self.token_settings_repo.delete()
            return OperationOutput(id=None, request="delete/token_settings", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 