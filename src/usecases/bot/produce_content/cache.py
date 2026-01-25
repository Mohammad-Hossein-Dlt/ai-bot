from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.request_model import RequestModel
from src.domain.schemas.user.user_model import UserModel
from typing import ClassVar

class ProduceContentCache:
    
    step: ClassVar[int] = 1
    
    def __init__(
        self,
        user_repo: IUserRepo,
        cache_repo: ICacheRepo,
        prompts: list[str],
        words_number: list[int],
        tones: list[str],
    ):
        self.user_repo = user_repo
        self.cache_repo = cache_repo
        self.prompts = prompts
        self.words_number = words_number
        self.tones = tones
    
    async def execute(
        self,
        chat_id: str,
        callback_data: CallbackDataRequest,
        entered_prompt: str | None = None,
    ) -> RequestModel:
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        
        cache_id = f"user:{user.id}:{chat_id}:request:{callback_data.message_id}"
        cache = self.cache_repo.get(cache_id)
        
        if cache:
            request: RequestModel = RequestModel.model_validate(cache)
        else:
            request: RequestModel = RequestModel()
        
        if callback_data.origin == "p":
            request.prompts.clear()
            request.prompts.append(self.prompts[callback_data.index])    
        elif callback_data.origin == "n":
            request.words_number = self.words_number[callback_data.index]    
        elif callback_data.origin == "t":
            if callback_data.index < 0:
                request.tones.remove(self.tones[abs(callback_data.index)])
            else:
                request.tones.append(self.tones[callback_data.index])
                
        if entered_prompt:
            request.entered_prompt = entered_prompt
            
        return RequestModel.model_validate(
            self.cache_repo.save(
                cache_id,
                request.model_dump(mode="json"),
                60 * 5,
            ),
        )
        