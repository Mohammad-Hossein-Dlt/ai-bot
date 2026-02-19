from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Icache import ICacheRepo
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.usecases.bot.get_conversation import GetConversation

from typing import ClassVar
import uuid
from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
)
from src.infra.utils.number_converter import english_to_persian, persian_to_english, number_formatter

class Payment:
    
    step: ClassVar[int] = 1
    
    def __init__(
        self,
        user_repo: IUserRepo,
        cache_repo: ICacheRepo,
        token_settings_repo: ITokenSettingsRepo,
        inline_keyboard: IInlineKeyboard,
    ):
        self.token_settings_repo = token_settings_repo
        self.inline_keyboard = inline_keyboard

        self.get_conversation_usecase = GetConversation(user_repo, cache_repo)
            
    async def execute(
        self,
        chat_id: str,
        callback_data: CallbackDataRequest,
    ):
        
        token_settings: TokenSettingsModel = await self.token_settings_repo.get()

        max_amount_formatted = english_to_persian(number_formatter(token_settings.max_tokens))
        min_amount_formatted = english_to_persian(number_formatter(token_settings.min_tokens))
        
        conversation = await self.get_conversation_usecase.execute(chat_id)
        tokens: str = conversation.messages.get("tokens", None)
        
        if not tokens.isnumeric():
            return 'لطفا عدد وارد کنید.', None

        tokens = int(persian_to_english(tokens))

        if tokens > token_settings.max_tokens:
            max_amount_error = f'تعداد وارد شده بیشتر از max عدد است.'
            max_amount_error = max_amount_error.replace('max', max_amount_formatted)
            return max_amount_error, None

        elif tokens < token_settings.min_tokens:
            min_amount_error = f'تعداد وارد شده کمتر از min عدد است.'
            min_amount_error = min_amount_error.replace('min', min_amount_formatted)
            return min_amount_error, None

        amount = tokens * token_settings.unit

        payment_id = str(uuid.uuid4())

        payment_url = f'{''}/api/v1/payment/request/?user_id={chat_id}&payment_id={payment_id}&amount={amount}&tokens={tokens}'

        payment_text = 'لینک پرداخت برای خرید تعداد توکن مورد نظر ساخته شد. از طریق لینک زیر پرداخت کنید.'
        
        self.inline_keyboard.add_row(
            {f"{english_to_persian(number_formatter(token_settings.unit))} ريال": "None1"},
            {"💵 قیمت هر توکن:": "None2"},
        )
        
        self.inline_keyboard.add_row(
            {f"{english_to_persian(number_formatter(tokens))} عدد": "None3"},
            {"💎 توکن درخواستی:": "None4"},
        )
        
        self.inline_keyboard.add_row(
            {f"{english_to_persian(number_formatter(amount))} ريال": "None5"},
            {"💰 قیمت:": "None6"},
        )
                
        self.inline_keyboard.add_row(
            {'✅ پرداخت': payment_url},
            {'🎁 اعمال کد تخفیف': callback_data.encode(step=self.step+1)},
        )

        self.inline_keyboard.add_row(
            {BACK: callback_data.encode(step=self.step-1, page=0)},
            {CLOSE_PANEL: f"close:{callback_data.message_id}"},
        )
        
        return payment_text, self.inline_keyboard.create_markup()