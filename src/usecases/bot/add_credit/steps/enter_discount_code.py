from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.models.schemas.bot.callback_request import CallbackDataRequest

from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
)

class EnterDiscountCode:
    
    def __init__(
        self,
        inline_keyboard: IInlineKeyboard,
    ):

        self.inline_keyboard = inline_keyboard
            
    async def execute(
        self,
        callback_data: CallbackDataRequest,
    ):
        
        enter_discount_code = "کد تخفیف مورد نظر را وارد کنید."
        
        back = Button(
            text=BACK,
            callback_data="back_from_cnvstn",
        )       
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )
        
        self.inline_keyboard.add_row(back, close)
        
        return enter_discount_code, self.inline_keyboard.create_markup()