from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.usecases.bot.save_conversation import SaveConversation
from src.usecases.bot.delete_conversation import DeleteConversation
from src.usecases.user.get_user_by_chat_id import GetUserByChatId
from src.usecases.token_settings.get_token_settings import GetTokenSettings
from src.usecases.category.get_category import GetCategory

from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.text_to_audio_request_model import TextToAudioRequestModel

from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.domain.schemas.category.category_model import CategoryModel

from src.infra.utils.number_converter import english_to_persian, number_formatter

from typing import ClassVar, Any
from raw_texts.raw_texts import (
    LACK_OF_CREDIT,
    BACK,
    CLOSE_PANEL,
)

class RequestSummary:
    
    step: ClassVar[int] = 2
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
        user_repo: IUserRepo,
        token_settings_repo: ITokenSettingsRepo,
        category_repo: ICategoryRepo,
        inline_keyboard: IInlineKeyboard,
        bot_platform: str,
    ):
        
        self.save_conversation_usecase = SaveConversation(cache_repo, user_repo)        
        self.delete_conversation_usecase = DeleteConversation(cache_repo, user_repo)
        self.get_user_by_chat_id_usecase = GetUserByChatId(user_repo, bot_platform)
        self.get_token_settings_usecase = GetTokenSettings(token_settings_repo)
        self.get_category_usecase = GetCategory(category_repo)
        
        self.inline_keyboard = inline_keyboard
        self.bot_platform = bot_platform
            
    async def execute(
        self,
        callback_data: CallbackDataRequest,
        request: TextToAudioRequestModel,
        chat_id: str,
    ) -> type[Any]:
        
        user: UserModel = await self.get_user_by_chat_id_usecase.execute(chat_id)
        token_settings: TokenSettingsModel = await self.get_token_settings_usecase.execute()
        model: CategoryModel = await self.get_category_usecase.execute(request.ai_model_id)
        
        wallet_validation = "" if user.tokens >= (model.tokens or token_settings.tokens_per_prompt) else LACK_OF_CREDIT
        
        text = "جزئیات درخواست:"
        
        text = f"{text.strip()}\n{wallet_validation}"
        
        back = Button(
            text=BACK,
            callback_data=callback_data.encode(step=self.step-1, page=0),
        )       
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )

        self.inline_keyboard.add_row(
            Button(text=model.ai_platform_type, callback_data="None-1"),
            Button(text="پلتفرم:", callback_data="None-2"),
        )
        
        self.inline_keyboard.add_row(
            Button(text=model.name, callback_data="None-3"),
            Button(text="مدل:", callback_data="None-4"),
        )
        
        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(model.tokens or token_settings.tokens_per_prompt))} توکن", callback_data="None-5"),
            Button(text="💵 هزینه تولید:", callback_data="None-6"),
        )
        
        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(int(user.tokens)))} توکن", callback_data="None-7"),
            Button(text="💎 اعتبار شما:", callback_data="None-8"),
        )        

        if user.tokens >= (model.tokens or token_settings.tokens_per_prompt):
            self.inline_keyboard.add_button(
                Button(text="ارسال پرامت 📄", callback_data="pv_cnvstn"),
            )

        self.inline_keyboard.add_row(back, close)
        
        await self.delete_conversation_usecase.execute(chat_id)
        await self.save_conversation_usecase.execute(chat_id, callback_data=callback_data)
        
        return text, self.inline_keyboard.create_markup()