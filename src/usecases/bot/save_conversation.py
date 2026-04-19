from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.bot.conversation_model import ConversationModel
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.domain.schemas.user.user_model import UserModel
from typing import ClassVar

class SaveConversation:
    
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
        callback_data: CallbackDataRequest | None = None,
        messages: dict | None = None,
    ) -> ConversationModel:
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        
        cache_id = f"user:{user.id}:{chat_id}:conversation"
        cache = self.cache_repo.get(cache_id)
        
        if callback_data:
            conversation: ConversationModel = ConversationModel(callback_data=callback_data)
        elif cache:
            conversation: ConversationModel = ConversationModel.model_validate(cache)

        if messages:
            conversation.messages = messages
            
        return ConversationModel.model_validate(
            self.cache_repo.save(
                cache_id,
                conversation.model_dump(mode="json"),
                60 * 5,
            ),
        )
        