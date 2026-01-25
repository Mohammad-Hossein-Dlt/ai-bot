from abc import ABC, abstractmethod
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel

class ITokenSettingsRepo(ABC):
        
    @abstractmethod
    async def create(
        token_settings: TokenSettingsModel,
    ) -> TokenSettingsModel:

        raise NotImplementedError
    
    @abstractmethod
    async def get() -> TokenSettingsModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        token_settings: TokenSettingsModel,
    ) -> TokenSettingsModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete() -> bool:
    
        raise NotImplementedError
