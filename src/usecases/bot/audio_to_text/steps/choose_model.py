from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.usecases.category.get_all_categories import GetAllCategories

from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.audio_to_text_request_model import AudioToTextRequestModel

from src.domain.schemas.category.category_model import CategoryModel
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.domain.enums import AiActionType

from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
)
from typing import ClassVar, Any

class ChooseModel:
    
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
        request: AudioToTextRequestModel,
    ) -> type[Any]:
        
        text = "مدل مورد نظر خود برای تبدیل صدا به متن رو انتخاب کنید."
        
        models: list[CategoryModel] = await self.get_all_categoryies_usecase.execute(
            CategoryFilterInput(
                ai_action_type=AiActionType.audio_to_text,
                ai_platform_type=request.ai_platform,
            ),
        )
                
        for index in callback_data.paginate:
            
            if index >= len(models): break
            
            model: CategoryModel = models[index]
            
            self.inline_keyboard.add_button(
                Button(
                    text=model.name,
                    callback_data=callback_data.encode(step=self.step+1, page=0, origin="am", index=index),
                ),
            )

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