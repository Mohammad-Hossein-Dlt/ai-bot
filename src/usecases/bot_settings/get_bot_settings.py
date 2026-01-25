from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.domain.schemas.bot_settings.bot_settings_model import BotSettingsModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetBotSettings:
    
    def __init__(
        self,
        settings_repo: IBotSettingsRepo,
    ):
        
        self.settings_repo = settings_repo
    
    async def execute(
        self,
    ) -> BotSettingsModel:
        
        try:
            return await self.settings_repo.get()
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 