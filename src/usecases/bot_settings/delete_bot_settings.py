from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteBotSettings:
    
    def __init__(
        self,
        settings_repo: IBotSettingsRepo,
    ):
        
        self.settings_repo = settings_repo
    
    async def execute(
        self,
    ) -> OperationOutput:
        
        try:
            status = await self.settings_repo.delete()
            return OperationOutput(id=None, request="delete/settings", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 