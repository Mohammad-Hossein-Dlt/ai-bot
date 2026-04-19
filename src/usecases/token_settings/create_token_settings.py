from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.models.schemas.token_settings.create_token_settings_input import CreateTokenSettingsInput
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateTokenSettings:
    
    def __init__(
        self,
        token_settings_repo: ITokenSettingsRepo,
    ):
        
        self.token_settings_repo = token_settings_repo
    
    async def execute(
        self,
        new_token_settings: CreateTokenSettingsInput,
    ) -> TokenSettingsModel:
        
        try:
            to_create: TokenSettingsModel = TokenSettingsModel.model_validate(new_token_settings, from_attributes=True)
            return await self.token_settings_repo.create(to_create)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 