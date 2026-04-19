from src.domain.enums import AiPlatformType, AiActionType
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.category.category_model import CategoryModel
from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.content_creation_request_model import ContentCreationRequestModel
from src.usecases.category.get_all_categories import GetAllCategories
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from typing import ClassVar

class ProduceContentCache:
    
    step: ClassVar[int] = 1
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
        user_repo: IUserRepo,
        category_repo: ICategoryRepo,
        prompts: list[str],
        words_number: list[int],
        tones: list[str],
    ):
        
        self.cache_repo = cache_repo
        self.user_repo = user_repo
        self.prompts = prompts
        self.words_number = words_number
        self.tones = tones
        
        self.get_all_categoryies_usecase = GetAllCategories(category_repo)

    
    async def execute(
        self,
        chat_id: str,
        callback_data: CallbackDataRequest,
    ) -> ContentCreationRequestModel:
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        
        cache_id = f"user:{user.id}:{chat_id}:request:{callback_data.message_id}"
        cache = self.cache_repo.get(cache_id)
        
        if cache:
            request: ContentCreationRequestModel = ContentCreationRequestModel.model_validate(cache)
        else:
            request: ContentCreationRequestModel = ContentCreationRequestModel()
        
        if callback_data.origin == "ap":
            ai_platforms = [platform.value for platform in AiPlatformType]
            request.ai_platform = ai_platforms[callback_data.index]
        elif callback_data.origin == "am":
            models = await self.get_all_categoryies_usecase.execute(
                CategoryFilterInput(
                    ai_platform_type=request.ai_platform,
                    ai_action_type=AiActionType.content_creation,
                ),
            )
            if models and len(models) > callback_data.index:
                selected_model: CategoryModel = models[callback_data.index]
                request.ai_model_id = str(selected_model.id)
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

        return ContentCreationRequestModel.model_validate(
            self.cache_repo.save(
                cache_id,
                request.model_dump(mode="json"),
                60 * 5,
            ),
        )
        