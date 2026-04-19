from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from typing import ClassVar

class DeleteConversation:
    
    step: ClassVar[int] = 1
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
        user_repo: IUserRepo,
    ):
        
        self.cache_repo = cache_repo
        self.user_repo = user_repo

    async def execute(
        self,
        chat_id: str,
    ) -> bool:
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        
        cache_id = f"user:{user.id}:{chat_id}:conversation"
        return self.cache_repo.delete(cache_id)