from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.infra.schemas.ai_client.ai_client import AiClient

from src.usecases.bot.get_conversation import GetConversation
from src.usecases.user.get_user_by_chat_id import GetUserByChatId
from src.usecases.user.modify_token_credit import ModifyUserTokenCredit
from src.usecases.token_settings.get_token_settings import GetTokenSettings
from src.usecases.category.get_category import GetCategory

from src.models.schemas.bot.content_creation_request_model import ContentCreationRequestModel

from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.domain.schemas.category.category_model import CategoryModel

from src.models.schemas.user.modify_user_token_credit_input import ModifyUserTokenCreditInput

from src.routes.bot.telegram.buttons import home_markup, back_markup
from src.infra.utils.pdf_generator import generate_pdf

from prompts.prompt_list import prompts, tone_prompt, words_number_prompt
from raw_texts.raw_texts import (
    LACK_OF_CREDIT,
    END_OF_CREATE_ARTICLE,
    RATE_LIMIT_ERROR,
)

import openai
from io import BytesIO
from typing import ClassVar, AsyncGenerator, Any

class Produce:
    
    step: ClassVar[int] = 6
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
        user_repo: IUserRepo,
        token_settings_repo: ITokenSettingsRepo,
        category_repo: ICategoryRepo,
        ai_client: AiClient,
        bot_platform: str,
    ):
        
        self.get_conversation_usecase = GetConversation(cache_repo, user_repo)
        self.get_user_by_chat_id_usecase = GetUserByChatId(user_repo, bot_platform)
        self.modify_user_token_credit_usecase = ModifyUserTokenCredit(user_repo, bot_platform)
        self.get_token_settings_usecase = GetTokenSettings(token_settings_repo)
        self.get_category_usecase = GetCategory(category_repo)
        
        self.ai_client = ai_client
        self.bot_platform = bot_platform
        
    async def execute(
        self,
        request: ContentCreationRequestModel,
        chat_id: str,
    ) -> AsyncGenerator[tuple[str, Any | None, BytesIO | None], None]:
        
        user: UserModel = await self.get_user_by_chat_id_usecase.execute(chat_id)
        token_settings: TokenSettingsModel = await self.get_token_settings_usecase.execute()
        model: CategoryModel = await self.get_category_usecase.execute(request.ai_model_id)

        if user.tokens < (model.tokens or token_settings.tokens_per_prompt):
            yield LACK_OF_CREDIT, home_markup, None
            
        conversation = await self.get_conversation_usecase.execute(chat_id)
        user_prompt = conversation.messages.get("prompt", None)
        
        
        def create_message(role: str, content: str) -> dict[str, str]:
            return {
                "role": role,
                "content": content,
            }
            
        try:
            yield "در حال پردازش...", back_markup, None
            
            completion = self.ai_client.open_ai_client.chat.completions.create(
                model=model.slug,
                store=True,
                messages=[
                    *[
                        create_message("system", prompts[p]) for p in request.prompts
                    ],
                    create_message(
                        "system",
                        tone_prompt.replace(
                            "<input_tone>", ", ".join(request.tones)
                        ),
                    ),
                    create_message("system", words_number_prompt.replace("<input_length>", str(request.words_number))),
                    create_message("system", "do not create image or table"),
                    create_message("user", user_prompt),
                ]
            )
            answer = completion.choices[0].message.content

        except openai.RateLimitError as e:
            yield RATE_LIMIT_ERROR, home_markup, None
        else:
            yield answer, home_markup, None
            pdf_file: BytesIO = generate_pdf(answer)
            yield END_OF_CREATE_ARTICLE, home_markup, pdf_file
            await self.modify_user_token_credit_usecase.execute(
                ModifyUserTokenCreditInput(
                    chat_id=chat_id,
                    bot_platform=self.bot_platform,
                    value=-(model.tokens or token_settings.tokens_per_prompt),
                ),
            )
        
