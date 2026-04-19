from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.usecases.bot.save_conversation import SaveConversation
from src.usecases.bot.get_conversation import GetConversation
from src.usecases.bot.delete_conversation import DeleteConversation
from src.usecases.user.get_user_by_chat_id import GetUserByChatId

from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.domain.schemas.user.user_model import UserModel

from typing import ClassVar
from raw_texts.raw_texts import CLOSE_PANEL
from src.infra.utils.number_converter import english_to_persian, number_formatter

class ShowCurrentCredit:
    
    step: ClassVar[int] = 0
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
        user_repo: IUserRepo,
        inline_keyboard: IInlineKeyboard,
        bot_platform: str,
    ):
        
        self.save_conversation_usecase = SaveConversation(cache_repo, user_repo)
        self.get_conversation_usecase = GetConversation(cache_repo, user_repo)
        self.delete_conversation_usecase = DeleteConversation(cache_repo, user_repo)
        self.get_user_by_chat_id = GetUserByChatId(user_repo, bot_platform)
            
        self.inline_keyboard = inline_keyboard
        
    async def execute(
        self,
        callback_data: CallbackDataRequest,
        chat_id: str,
    ):
        
        user: UserModel = await self.get_user_by_chat_id.execute(chat_id)

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
        conversation = await self.get_conversation_usecase.execute(chat_id)
        await self.save_conversation_usecase.execute(
            chat_id,
            callback_data=callback_data,
            messages=conversation.messages if conversation else [],
        )
        
        return wallet_credit, self.inline_keyboard.create_markup()
        