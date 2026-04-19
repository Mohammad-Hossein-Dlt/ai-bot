from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.models.schemas.bot_settings.update_bot_settings_input import UpdateBotSettingsInput
from src.domain.schemas.bot_settings.bot_settings_model import BotSettingsModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateBotSettings:
    
    def __init__(
        self,
        settings_repo: IBotSettingsRepo,
    ):
        
        self.settings_repo = settings_repo
    
    async def execute(
        self,
        bot_settings: UpdateBotSettingsInput,
    ) -> BotSettingsModel:
        
        try:
            to_update: BotSettingsModel = BotSettingsModel.model_validate(bot_settings, from_attributes=True)
            return await self.settings_repo.update(to_update)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 