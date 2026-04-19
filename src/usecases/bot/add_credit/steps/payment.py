from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.usecases.bot.get_conversation import GetConversation
from src.usecases.payment.create_payment import CreatePayment
from src.usecases.token_settings.get_token_settings import GetTokenSettings

from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.models.schemas.payment.create_payment_input import CreatePaymentInput

from src.infra.utils.number_converter import english_to_persian, persian_to_english, number_formatter
from raw_texts.raw_texts import CLOSE_PANEL
from typing import ClassVar

class Payment:
    
    step: ClassVar[int] = 2
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
        user_repo: IUserRepo,
        token_settings_repo: ITokenSettingsRepo,
        payment_repo: IPaymentRepo,
        payment_service: IPaymentService,
        bot_platform: str,
        inline_keyboard: IInlineKeyboard,
    ):
        
        self.get_conversation_usecase = GetConversation(cache_repo, user_repo)
        self.create_payment_usecase = CreatePayment(user_repo, payment_repo, payment_service, bot_platform)
        self.get_token_settings_usecase = GetTokenSettings(token_settings_repo)
            
        self.inline_keyboard = inline_keyboard
        
    async def execute(
        self,
        callback_data: CallbackDataRequest,
        chat_id: str,
    ):
        
        token_settings: TokenSettingsModel = await self.get_token_settings_usecase.execute()

        max_amount_formatted = english_to_persian(number_formatter(token_settings.max_tokens))
        min_amount_formatted = english_to_persian(number_formatter(token_settings.min_tokens))
        
        conversation = await self.get_conversation_usecase.execute(chat_id)
        entered_tokens: str = conversation.messages.get("tokens", None)
        entered_discount_code: str = conversation.messages.get("discount_code", None)
        
        if not entered_tokens.isnumeric():
            return 'لطفا عدد وارد کنید.', None

        entered_tokens = int(persian_to_english(entered_tokens))

        if entered_tokens > token_settings.max_tokens:
            max_amount_error = f'تعداد وارد شده بیشتر از max عدد است.'
            max_amount_error = max_amount_error.replace('max', max_amount_formatted)
            return max_amount_error, None

        elif entered_tokens < token_settings.min_tokens:
            min_amount_error = f'تعداد وارد شده کمتر از min عدد است.'
            min_amount_error = min_amount_error.replace('min', min_amount_formatted)
            return min_amount_error, None

        amount = entered_tokens * token_settings.unit

        # payment_id = str(uuid.uuid4())
        # payment_url = f'{'http://localhost'}/api/v1/payment/request/?user_id={chat_id}&payment_id={payment_id}&amount={amount}&tokens={tokens}'
        
        payment = await self.create_payment_usecase.execute(
            CreatePaymentInput(
                chat_id=str(chat_id),
                amount=amount,
                tokens=entered_tokens,
            ),
        )

        payment_text = 'لینک پرداخت برای خرید تعداد توکن مورد نظر ساخته شد. از طریق لینک زیر پرداخت کنید.'
             
                
        self.inline_keyboard.add_row(
            Button(text='✅ پرداخت', callback_data=payment.payment_link, is_link=True),
        )
        
        self.inline_keyboard.add_row(
            Button(text=CLOSE_PANEL, callback_data=f"close:{callback_data.message_id}"),
        )
        
        return payment_text, self.inline_keyboard.create_markup()