from abc import ABC, abstractmethod
from src.domain.schemas.user.user_model import UserModel

class IUserRepo(ABC):
        
    @abstractmethod
    async def create(
        user: UserModel,
    ) -> UserModel:

        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(
        user_id: str,
    ) -> UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_chat_id(
        chat_id: int | str,
        bot_platform: str | None = None,
    ) -> UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update(
        user: UserModel,
    ) -> UserModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def modify_token_credit(
        user: UserModel,
        value: int,
    ) -> UserModel:
    
        raise NotImplementedError
        
    @abstractmethod
    async def modify_token_credit_for_all_users(
        value: int,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_id(
        user_id: str,
    ) -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_by_chat_id(
        chat_id: int | str,
        bot_platform: str | None = None,
    ) -> bool:
    
        raise NotImplementedError
