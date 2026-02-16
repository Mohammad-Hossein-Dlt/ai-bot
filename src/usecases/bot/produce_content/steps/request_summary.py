from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Icache import ICacheRepo
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.domain.schemas.user.user_model import UserModel
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.request_model import RequestModel
from src.usecases.bot.save_conversation import SaveConversation
from typing import ClassVar, Any
from raw_texts.raw_texts import (
    LACK_OF_CREDIT,
    PRODUCE_CONTENT_INFO,
    BACK,
    CLOSE_PANEL,
)
from src.infra.utils.number_converter import english_to_persian, number_formatter

class RequestSummary:
    
    step: ClassVar[int] = 3
    
    def __init__(
        self,
        user_repo: IUserRepo,
        token_settings_repo: ITokenSettingsRepo,
        cache_repo: ICacheRepo,
        inline_keyboard: IInlineKeyboard,
    ):
        self.user_repo = user_repo
        self.token_settings_repo = token_settings_repo
        self.cache_repo = cache_repo
        self.inline_keyboard = inline_keyboard
        
        self.save_conversation_usecase = SaveConversation(user_repo, cache_repo)
    
    async def execute(
        self,
        chat_id: str,
        request: RequestModel,
        callback_data: CallbackDataRequest,
    ) -> type[Any]:
        
        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        token_settings: TokenSettingsModel = await self.token_settings_repo.get()

        wallet_validation = "" if user.tokens >= token_settings.tokens_per_prompt else LACK_OF_CREDIT
        text = PRODUCE_CONTENT_INFO.replace(
            "category",
            "، ".join(request.prompts),
        ).replace(
            "words_length",
            str(request.words_number),
        ).replace(
            "tone",
            "، ".join(request.tones),
        )
        
        text = f"{text.strip()}\n{wallet_validation}"

        self.inline_keyboard.add_row(
            {f"{english_to_persian(number_formatter(token_settings.tokens_per_prompt))} توکن": "None1"},
            {"💵 هزینه تولید:": "None2"},
        )
        
        self.inline_keyboard.add_row(
            {f"{english_to_persian(number_formatter(int(user.tokens)))} توکن": "None3"},
            {"💎 اعتبار شما:": "None4"},
        )        

        if user.tokens >= token_settings.tokens_per_prompt:
            self.inline_keyboard.add_button(
                "ارسال پرامت 📄",
                "conversation",
            )

        self.inline_keyboard.add_row(
            {BACK: callback_data.encode(step=self.step-1, page=0)},
            {CLOSE_PANEL: f"close:{callback_data.message_id}"},
        )
        
        await self.save_conversation_usecase.execute(chat_id, callback_data=callback_data)
        
        return text, self.inline_keyboard.create_markup()