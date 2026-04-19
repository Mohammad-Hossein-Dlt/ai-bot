from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.usecases.category.get_all_categories import GetAllCategories

from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.pricing import PricingRequestModel

from src.domain.schemas.category.category_model import CategoryModel
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.domain.enums import AiActionType

from raw_texts.raw_texts import (
    CONTENT_CREATION,
    TEXT_TO_IMAGE,
    TEXT_TO_AUDIO,
    AUDIO_TO_TEXT,
    BACK,
    CLOSE_PANEL,
)
from typing import ClassVar, Any

class CategoriesPriceAmount:
    
    step: ClassVar[int] = 1
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
        inline_keyboard: IInlineKeyboard,
    ):

        self.get_all_categoryies_usecase = GetAllCategories(category_repo)
        
        self.inline_keyboard = inline_keyboard
    
    async def execute(
        self,
        callback_data: CallbackDataRequest,
        request: PricingRequestModel,
    ) -> type[Any]:
        
        text = ""
        
        pairs = {
            CONTENT_CREATION: AiActionType.content_creation,
            TEXT_TO_IMAGE: AiActionType.text_to_image,
            TEXT_TO_AUDIO: AiActionType.text_to_audio,
            AUDIO_TO_TEXT: AiActionType.audio_to_text,
        }
        
        models: list[CategoryModel] = await self.get_all_categoryies_usecase.execute(
            CategoryFilterInput(
                ai_action_type=pairs[request.ai_action_type_fa],
            ),
        )
        
        for index in callback_data.paginate:
            if index >= len(models): break
            model: CategoryModel = models[index]
            text += "\n" + "💎 " + model.name + "\n" + "💰 " + str(model.tokens) + " توکن "

        previous_page = Button(
            text="صفحه قبلی ⬅️",
            callback_data=callback_data.encode(step=self.step, page=callback_data.page-1) if callback_data.page is not None else None,
        )
        next_page = Button(
            text="➡️ صفحه بعدی",
            callback_data=callback_data.encode(step=self.step, page=callback_data.page+1) if callback_data.page is not None else None,
        )
        
        back = Button(
            text=BACK,
            callback_data=callback_data.encode(step=self.step-1, page=0),
        ) 
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )
        
        if callback_data.start > 0 and callback_data.end < len(models):
            self.inline_keyboard.add_row(previous_page, next_page)
        elif callback_data.start > 0:
            self.inline_keyboard.add_row(previous_page)
        elif callback_data.end < len(models):
            self.inline_keyboard.add_row(next_page)

        self.inline_keyboard.add_row(back, close)
        
        return text, self.inline_keyboard.create_markup()