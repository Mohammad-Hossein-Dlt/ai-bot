from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.models.schemas.bot_settings.create_bot_settings_input import CreateBotSettingsInput
from src.domain.schemas.bot_settings.bot_settings_model import BotSettingsModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateBotSettings:
    
    def __init__(
        self,
        settings_repo: IBotSettingsRepo,
    ):
        
        self.settings_repo = settings_repo
    
    async def execute(
        self,
        new_bot_settings: CreateBotSettingsInput,
    ) -> BotSettingsModel:
        
        try:
            to_create: BotSettingsModel = BotSettingsModel.model_validate(new_bot_settings, from_attributes=True)
            return await self.settings_repo.create(to_create)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 