from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.domain.enums import AiPlatformType

from typing import ClassVar, Any
from raw_texts.raw_texts import (
    CLOSE_PANEL,
)

class ChooseAiPlatform:
    
    step: ClassVar[int] = 0
    
    def __init__(
        self,
        inline_keyboard: IInlineKeyboard,
    ):
        
        self.inline_keyboard = inline_keyboard
    
    def execute(
        self,
        callback_data: CallbackDataRequest,
    ) -> type[Any]:
        
        text = "پلتفرم مورد نظر خود برای تولید تصویر رو انتخاب کنید."
        
        ai_platforms = [platform.value for platform in AiPlatformType]
                
        for index in callback_data.paginate:
            if index >= len(ai_platforms): break
            self.inline_keyboard.add_button(
                Button(
                    text=ai_platforms[index],
                    callback_data=callback_data.encode(step=self.step+1, page=0, origin="ap", index=index),
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
        
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )
        
        if callback_data.start > 0 and callback_data.end < len(ai_platforms):
            self.inline_keyboard.add_row(previous_page, next_page)
        elif callback_data.start > 0:
            self.inline_keyboard.add_row(previous_page)
        elif callback_data.end < len(ai_platforms):
            self.inline_keyboard.add_row(next_page)

        self.inline_keyboard.add_button(close)
        
        return text, self.inline_keyboard.create_markup()