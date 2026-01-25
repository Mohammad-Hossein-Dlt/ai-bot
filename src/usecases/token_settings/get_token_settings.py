from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetTokenSettings:
    
    def __init__(
        self,
        token_settings_repo: ITokenSettingsRepo,
    ):
        
        self.token_settings_repo = token_settings_repo
    
    async def execute(
        self,
    ) -> TokenSettingsModel:
        
        try:
            return await self.token_settings_repo.get()
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 