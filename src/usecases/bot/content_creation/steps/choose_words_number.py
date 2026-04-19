from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.models.schemas.bot.callback_request import CallbackDataRequest

from typing import ClassVar, Any
from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
)

class ChooseWordsNumber:
    
    step: ClassVar[int] = 3
    
    def __init__(
        self,
        words_number: list[int],
        inline_keyboard: IInlineKeyboard,
    ):
        self.words_number = words_number
        self.inline_keyboard = inline_keyboard
    
    def execute(
        self,
        callback_data: CallbackDataRequest,
    ) -> type[Any]:
        
        text = "تعداد کلمات پاسخ تولیدی را انتخاب کنید"

        for index, value in enumerate(self.words_number):
            self.inline_keyboard.add_button(
                Button(
                    text=str(value),
                    callback_data=callback_data.encode(step=self.step+1, page=0, origin="n", index=index),
                )
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

        if callback_data.start > 0 and callback_data.end < len(self.words_number):
            self.inline_keyboard.add_row(previous_page, next_page)
        elif callback_data.start > 0:
            self.inline_keyboard.add_row(previous_page)
        elif callback_data.end < len(self.words_number):
            self.inline_keyboard.add_row(next_page)
        
        self.inline_keyboard.add_row(back, close)
        
        return text, self.inline_keyboard.create_markup()
        