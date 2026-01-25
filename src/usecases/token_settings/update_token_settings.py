from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.models.schemas.token_settings.update_token_settings_input import UpdateTokenSettingsInput
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateTokenSettings:
    
    def __init__(
        self,
        token_settings_repo: ITokenSettingsRepo,
    ):
        
        self.token_settings_repo = token_settings_repo
    
    async def execute(
        self,
        settings: UpdateTokenSettingsInput,
    ) -> TokenSettingsModel:
        
        try:
            to_update: TokenSettingsModel = TokenSettingsModel.model_validate(settings, from_attributes=True)
            return await self.token_settings_repo.update(to_update)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 