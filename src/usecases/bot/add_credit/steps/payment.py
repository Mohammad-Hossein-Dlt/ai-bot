from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Icache import ICacheRepo
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import Button, IInlineKeyboard
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

        payment_url = f'{'http://localhost'}/api/v1/payment/request/?user_id={chat_id}&payment_id={payment_id}&amount={amount}&tokens={tokens}'

        payment_text = 'لینک پرداخت برای خرید تعداد توکن مورد نظر ساخته شد. از طریق لینک زیر پرداخت کنید.'

        back = Button(
            text=BACK,
            callback_data=callback_data.encode(step=self.step-1, page=0),
        )       
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )        

        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(token_settings.unit))} ريال", callback_data="None1"),
            Button(text="💵 قیمت هر توکن:", callback_data="None2"),
        )
        
        self.inline_keyboard.add_row(
            Button(f"{english_to_persian(number_formatter(tokens))} عدد", callback_data="None3"),
            Button(text="💎 توکن درخواستی:", callback_data="None4"),
        )
        
        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(amount))} ريال", callback_data="None5"),
            Button("💰 قیمت:", callback_data="None6"),
        )
                
        self.inline_keyboard.add_row(
            Button(text='✅ پرداخت', callback_data=payment_url, is_link=True),
            Button(text='🎁 اعمال کد تخفیف', callback_data=callback_data.encode(step=self.step+1)),
        )
        
        self.inline_keyboard.add_row(back, close)

        return payment_text, self.inline_keyboard.create_markup()