from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Icache import ICacheRepo
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.domain.schemas.user.user_model import UserModel
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.models.schemas.bot.text_to_image_request_model import TextToImageRequestModel

from src.usecases.bot.get_conversation import GetConversation

from src.routes.bot.telegram.general_buttons import home_markup, back_markup

from raw_texts.raw_texts import (
    LACK_OF_CREDIT,
    END_OF_CREATE_ARTICLE,
    RATE_LIMIT_ERROR,
)

import openai
from openai import OpenAI
from io import BytesIO
import base64
from typing import ClassVar, AsyncGenerator, Any

class Produce:
    
    step: ClassVar[int] = 2
    
    def __init__(
        self,
        user_repo: IUserRepo,
        token_settings_repo: ITokenSettingsRepo,
        cache_repo: ICacheRepo,
        gpt_client: OpenAI,
        inline_keyboard: IInlineKeyboard,
    ):
        self.user_repo = user_repo
        self.token_settings_repo = token_settings_repo
        self.cache_repo = cache_repo
        self.gpt_client = gpt_client
        self.inline_keyboard = inline_keyboard
        
        self.get_conversation_usecase = GetConversation(user_repo, cache_repo)
    
    async def execute(
        self,
        chat_id: str,
        request: TextToImageRequestModel,
    ) -> AsyncGenerator[tuple[str, Any | None, BytesIO | None], None]:
        
        token_settings: TokenSettingsModel = await self.token_settings_repo.get()

        user: UserModel = await self.user_repo.get_by_chat_id(chat_id)

        if user.tokens < token_settings.tokens_per_prompt:
            yield LACK_OF_CREDIT, home_markup, None
            
        conversation = await self.get_conversation_usecase.execute(chat_id)
        user_prompt = conversation.messages.get("prompt", None)
            
        try:
            # yield "در حال پردازش...", back_markup, None
            yield "در حال پردازش...", home_markup, None
            result = self.gpt_client.images.generate(
                model="gpt-image-1-mini",
                prompt=user_prompt,
                size="1024x1024"
            )
        except openai.RateLimitError as e:
            yield RATE_LIMIT_ERROR, home_markup, None
        else:
            b64 = result.data[0].b64_json
            image: BytesIO = BytesIO()
            image.write(base64.b64decode(b64))
            image.seek(0)
            yield END_OF_CREATE_ARTICLE, home_markup, image
            await self.user_repo.modify_token_credit(chat_id, -token_settings.tokens_per_prompt)
        
