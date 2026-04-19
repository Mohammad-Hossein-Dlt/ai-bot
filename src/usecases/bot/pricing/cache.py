from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.pricing import PricingRequestModel

class PricingCache:
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
        user_repo: IUserRepo,
        ai_action_type_fa: list[str],
    ):
        
        self.cache_repo = cache_repo  
        self.user_repo = user_repo
        self.ai_action_type_fa = ai_action_type_fa
                    
    async def execute(
        self,
        chat_id: str,
        callback_data: CallbackDataRequest,
    ) -> PricingRequestModel:
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        
        cache_id = f"user:{user.id}:{chat_id}:request:{callback_data.message_id}"
        cache = self.cache_repo.get(cache_id)
        
        if cache:
            request: PricingRequestModel = PricingRequestModel.model_validate(cache)
        else:
            request: PricingRequestModel = PricingRequestModel()
        
        if callback_data.origin == "aatfa":
            request.ai_action_type_fa = self.ai_action_type_fa[callback_data.index]
                
        return PricingRequestModel.model_validate(
            self.cache_repo.save(
                cache_id,
                request.model_dump(mode="json"),
                60 * 5,
            ),
        )
        