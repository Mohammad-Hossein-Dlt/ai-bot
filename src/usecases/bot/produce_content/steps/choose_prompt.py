from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.models.schemas.bot.callback_request import CallbackDataRequest
from typing import ClassVar, Any
from raw_texts.raw_texts import (
    CLOSE_PANEL,
)

class ChoosePrompt:
    
    step: ClassVar[int] = 0
    
    def __init__(
        self,
        prompts: list[str],
        inline_keyboard: IInlineKeyboard,
    ):
        self.prompts = prompts
        self.inline_keyboard = inline_keyboard
    
    def execute(
        self,
        callback_data: CallbackDataRequest,
    ) -> type[Any]:
        
        text = 'موضوع درخواستی خود را انتخاب کنید.'
                
        for index in callback_data.paginate:
            if index >= len(self.prompts): break
            self.inline_keyboard.add_button(
                self.prompts[index],
                callback_data.encode(step=self.step+1, page=0, origin="p", index=index),
            )

        previous_page = {"صفحه قبلی ⬅️": callback_data.encode(step=self.step, page=callback_data.page-1)} if callback_data.page is not None else None
        next_page = {"➡️ صفحه بعدی": callback_data.encode(step=self.step, page=callback_data.page+1)} if callback_data.page is not None else None
        
        if callback_data.start > 0 and callback_data.end < len(self.prompts):
            self.inline_keyboard.add_row(previous_page, next_page)
        elif callback_data.start > 0:
            self.inline_keyboard.add_row(previous_page)
        elif callback_data.end < len(self.prompts):
            self.inline_keyboard.add_row(next_page)

        self.inline_keyboard.add_button(CLOSE_PANEL, f"close:{callback_data.message_id}")
        
        return text, self.inline_keyboard.create_markup()