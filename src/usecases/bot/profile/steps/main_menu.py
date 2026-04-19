from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.domain.schemas.user.user_model import UserModel

from src.infra.utils.number_converter import english_to_persian, number_formatter
from raw_texts.raw_texts import CLOSE_PANEL
from typing import ClassVar

class MainMenu:
    
    step: ClassVar[int] = 0
    
    def __init__(
        self,
        user_repo: IUserRepo,
        inline_keyboard: IInlineKeyboard,
    ):
        
        self.user_repo = user_repo
        self.inline_keyboard = inline_keyboard
        
    async def execute(
        self,
        callback_data: CallbackDataRequest,
        chat_id: str,
    ):
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
    
        text = f"شناسه کاربری شما: user_id"
        text = text.replace("user_id", str(chat_id))
        
        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(int(user.tokens)))} عدد", callback_data="None-1"),
            Button(text="💎 توکن‌های‌شما", callback_data="None-2"),
        )
        
        self.inline_keyboard.add_row(
            Button(text=CLOSE_PANEL, callback_data=f"close:{callback_data.message_id}")
        )
        
        return text, self.inline_keyboard.create_markup()