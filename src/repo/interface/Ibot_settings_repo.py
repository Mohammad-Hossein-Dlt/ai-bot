from abc import ABC, abstractmethod
from src.domain.schemas.bot_settings.bot_settings_model import BotSettingsModel

class IBotSettingsRepo(ABC):
        
    @abstractmethod
    async def create(
        settings: BotSettingsModel,
    ) -> BotSettingsModel:

        raise NotImplementedError
    
    @abstractmethod
    async def get() -> BotSettingsModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        settings: BotSettingsModel,
    ) -> BotSettingsModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete() -> bool:
    
        raise NotImplementedError
