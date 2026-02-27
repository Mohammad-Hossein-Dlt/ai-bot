from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Icache import ICacheRepo
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.domain.schemas.user.user_model import UserModel
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import Button, IInlineKeyboard
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.models.schemas.bot.produce_content_request_model import ProduceContentRequestModel
from src.usecases.bot.save_conversation import SaveConversation
from src.usecases.bot.delete_conversation import DeleteConversation
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
        self.delete_conversation_usecase = DeleteConversation(user_repo, cache_repo)
    
    async def execute(
        self,
        chat_id: str,
        request: ProduceContentRequestModel,
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
        
        back = Button(
            text=BACK,
            callback_data=callback_data.encode(step=self.step-1, page=0),
        )       
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )

        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(token_settings.tokens_per_prompt))} توکن", callback_data="None1"),
            Button(text="💵 هزینه تولید:", callback_data="None2"),
        )
        
        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(int(user.tokens)))} توکن", callback_data="None3"),
            Button(text="💎 اعتبار شما:", callback_data="None4"),
        )        

        if user.tokens >= token_settings.tokens_per_prompt:
            self.inline_keyboard.add_button(
                Button(text="ارسال پرامت 📄", callback_data="pc_cnvstn"),
            )

        self.inline_keyboard.add_row(back, close)
        
        await self.delete_conversation_usecase.execute(chat_id)
        await self.save_conversation_usecase.execute(chat_id, callback_data=callback_data)
        
        return text, self.inline_keyboard.create_markup()