from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Icache import ICacheRepo
from src.domain.schemas.user.user_model import UserModel
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import Button, IInlineKeyboard
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.usecases.bot.save_conversation import SaveConversation
from src.usecases.bot.delete_conversation import DeleteConversation
from typing import ClassVar
from raw_texts.raw_texts import (
    CLOSE_PANEL,
)
from src.infra.utils.number_converter import english_to_persian, number_formatter

class ShowCurrentCredit:
    
    step: ClassVar[int] = 0
    
    def __init__(
        self,
        user_repo: IUserRepo,
        cache_repo: ICacheRepo,
        inline_keyboard: IInlineKeyboard,
    ):
        self.user_repo = user_repo
        self.inline_keyboard = inline_keyboard
        
        self.save_conversation_usecase = SaveConversation(user_repo, cache_repo)
        self.delete_conversation_usecase = DeleteConversation(user_repo, cache_repo)
            
    async def execute(
        self,
        chat_id: str,
        callback_data: CallbackDataRequest,
    ):
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)

        if not user:
            return 'کاربر وجود ندارد!', None

        wallet_credit = f"شناسه کاربری شما: user_id"
        wallet_credit = wallet_credit.replace("user_id", str(chat_id))
        
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )
        
        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(int(user.tokens)))} عدد", callback_data="None2"),
            Button(text="💎 توکن‌های‌شما", callback_data="None1"),
        )
        
        self.inline_keyboard.add_row(
            Button(text="خرید توکن 💳", callback_data="ac_cnvstn"),
        )
        
        self.inline_keyboard.add_row(close)        

        await self.delete_conversation_usecase.execute(chat_id)
        await self.save_conversation_usecase.execute(chat_id, callback_data=callback_data)
        
        return wallet_credit, self.inline_keyboard.create_markup()
        