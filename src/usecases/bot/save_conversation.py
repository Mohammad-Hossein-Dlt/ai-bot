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
        user_repo: IUserRepo,
        cache_repo: ICacheRepo,
    ):
        self.user_repo = user_repo
        self.cache_repo = cache_repo

    async def execute(
        self,
        chat_id: str,
        callback_data: CallbackDataRequest | None = None,
        message: dict | None = None,
    ) -> ConversationModel:
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        
        cache_id = f"user:{user.id}:{chat_id}:conversation"
        cache = self.cache_repo.get(cache_id)
        
        if cache:
            conversation: ConversationModel = ConversationModel.model_validate(cache)
        elif callback_data:
            conversation: ConversationModel = ConversationModel(callback_data=callback_data)

        if message:
            conversation.messages.update(**message)
            
        return ConversationModel.model_validate(
            self.cache_repo.save(
                cache_id,
                conversation.model_dump(mode="json"),
                60 * 5,
            ),
        )
        