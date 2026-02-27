from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import Button, IInlineKeyboard
from src.models.schemas.bot.callback_request import CallbackDataRequest
from typing import ClassVar, Any
from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
    ENTER_SUBJECT,
)

class EnterPrompt:
    
    step: ClassVar[int] = 4
    
    def __init__(
        self,
        inline_keyboard: IInlineKeyboard,
    ):
        self.inline_keyboard = inline_keyboard
    
    async def execute(
        self,
        callback_data: CallbackDataRequest,
    ) -> type[Any]:

        back = Button(
            text=BACK,
            callback_data="back_from_cnvstn",
        )       
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )
        
        self.inline_keyboard.add_row(back, close)

        return ENTER_SUBJECT, self.inline_keyboard.create_markup()