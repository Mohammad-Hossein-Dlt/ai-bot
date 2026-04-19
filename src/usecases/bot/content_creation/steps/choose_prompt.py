from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.models.schemas.bot.callback_request import CallbackDataRequest

from typing import ClassVar, Any
from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
)

class ChoosePrompt:
    
    step: ClassVar[int] = 2
    
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
                Button(
                    text=self.prompts[index],
                    callback_data=callback_data.encode(step=self.step+1, page=0, origin="p", index=index),
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
        
        if callback_data.start > 0 and callback_data.end < len(self.prompts):
            self.inline_keyboard.add_row(previous_page, next_page)
        elif callback_data.start > 0:
            self.inline_keyboard.add_row(previous_page)
        elif callback_data.end < len(self.prompts):
            self.inline_keyboard.add_row(next_page)

        self.inline_keyboard.add_row(back, close)
        
        return text, self.inline_keyboard.create_markup()