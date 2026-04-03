from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.text_to_audio_request_model import TextToAudioRequestModel
from src.domain.schemas.user.user_model import UserModel
from typing import ClassVar

class ProduceAudioCache:
    
    step: ClassVar[int] = 1
    
    def __init__(
        self,
        user_repo: IUserRepo,
        cache_repo: ICacheRepo,
        ai_platforms: list[str],
    ):
        self.user_repo = user_repo
        self.cache_repo = cache_repo    
        self.ai_platforms = ai_platforms
            
    async def execute(
        self,
        chat_id: str,
        callback_data: CallbackDataRequest,
    ) -> TextToAudioRequestModel:
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        
        cache_id = f"user:{user.id}:{chat_id}:request:{callback_data.message_id}"
        cache = self.cache_repo.get(cache_id)
        
        if cache:
            request: TextToAudioRequestModel = TextToAudioRequestModel.model_validate(cache)
        else:
            request: TextToAudioRequestModel = TextToAudioRequestModel()
        
        if callback_data.origin == "ap":
            request.ai_platform = self.ai_platforms[callback_data.index]

        return TextToAudioRequestModel.model_validate(
            self.cache_repo.save(
                cache_id,
                request.model_dump(mode="json"),
                60 * 5,
            ),
        )
        