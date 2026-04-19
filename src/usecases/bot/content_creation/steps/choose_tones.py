from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.content_creation_request_model import ContentCreationRequestModel

from typing import ClassVar, Any
from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
)

class ChooseTones:
    
    step: ClassVar[int] = 4
    
    def __init__(
        self,
        tones: list[str],
        inline_keyboard: IInlineKeyboard,
    ):
        
        self.tones = tones
        self.inline_keyboard = inline_keyboard
    
    def execute(
        self,
        callback_data: CallbackDataRequest,
        request: ContentCreationRequestModel,
    ) -> type[Any]:

        text = 'لحن را انتخاب کنید.' + '\n' + 'میتوانید چند نوع را انتخاب کنید.' + '\n\n' + 'سپس گزینه تولید که در انتهای لیست لحن قرار دارد را انتخاب نمایید.'

        selected_tones = request.tones.copy()

        if len(selected_tones) != 0:
            text += '\n' + 'انتخاب شده: ' + '، '.join(selected_tones)

        for index in callback_data.paginate:
           
            if index >= len(self.tones):
                break
            
            value = self.tones[index]
            to_callback = callback_data.encode(step=self.step, page=callback_data.page, origin="t", index=index)
            
            if value in selected_tones:
                value += " ✅️ "
                to_callback = callback_data.encode(step=self.step, page=callback_data.page, origin="t", index=-index)
            
            self.inline_keyboard.add_button(
                Button(
                    text=value,
                    callback_data=to_callback,
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
        produce = Button(
            text="ادامه ⚡️",
            callback_data=callback_data.encode(step=self.step+1),
        )
        
        back = Button(
            text=BACK,
            callback_data=callback_data.encode(step=self.step-1, page=0),
        )       
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )
        
        if callback_data.start > 0 and callback_data.end < len(self.tones):
            self.inline_keyboard.add_row(previous_page, next_page)
        elif callback_data.start > 0:
            self.inline_keyboard.add_row(previous_page)
        elif callback_data.end < len(self.tones):
            self.inline_keyboard.add_row(next_page)

        if len(selected_tones) != 0:
            self.inline_keyboard.add_column(produce)
            
        self.inline_keyboard.add_row(back, close)
        
        return text, self.inline_keyboard.create_markup()