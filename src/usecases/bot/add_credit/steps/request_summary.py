from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard, Button

from src.usecases.bot.get_conversation import GetConversation
from src.usecases.bot.save_conversation import SaveConversation
from src.usecases.token_settings.get_token_settings import GetTokenSettings
from src.usecases.discount_code.get_discount_code_by_code import GetDiscountCodeByCode

from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.domain.schemas.discount_code.discount_code_model import DiscountCodeModel

from src.infra.utils.number_converter import english_to_persian, persian_to_english, number_formatter
from src.infra.exceptions.exceptions import EntityNotFoundError

from typing import ClassVar
from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
)

class RequestSummary:
    
    step: ClassVar[int] = 1
    
    def __init__(
        self,
        cache_repo: ICacheRepo,
        user_repo: IUserRepo,
        token_settings_repo: ITokenSettingsRepo,
        discount_code_repo: IDiscountCodeRepo,
        inline_keyboard: IInlineKeyboard,
    ):

        self.get_conversation_usecase = GetConversation(cache_repo, user_repo)
        self.save_conversation_usecase = SaveConversation(cache_repo, user_repo)
        # self.delete_conversation_usecase = DeleteConversation(cache_repo, user_repo)
        self.get_token_settings_usecase = GetTokenSettings(token_settings_repo)
        self.get_discount_code_by_code_usecase = GetDiscountCodeByCode(discount_code_repo)
            
        self.inline_keyboard = inline_keyboard
        
    async def execute(
        self,
        callback_data: CallbackDataRequest,
        chat_id: str,
    ):
        
        token_settings: TokenSettingsModel = await self.get_token_settings_usecase.execute()

        unit_formatted = english_to_persian(number_formatter(token_settings.unit))
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

        payment_text = 'لینک پرداخت برای خرید تعداد توکن مورد نظر ساخته شد. از طریق لینک زیر پرداخت کنید.'
        payment_text += "\n" + f"قیمت هر توکن: *{unit_formatted}* تومان"

        amount = entered_tokens * token_settings.unit
        
        discount_code: DiscountCodeModel = None
        if entered_discount_code:
            try:
                discount_code: DiscountCodeModel = await self.get_discount_code_by_code_usecase.execute(entered_discount_code)
            except EntityNotFoundError:
                payment_text += "\n" + "❌ کد تخفیف یافت نشد!"

        back = Button(
            text=BACK,
            callback_data=callback_data.encode(step=self.step-1, page=0),
        )       
        close = Button(
            text=CLOSE_PANEL,
            callback_data=f"close:{callback_data.message_id}",
        )        

        self.inline_keyboard.add_row(
            Button(f"{english_to_persian(number_formatter(entered_tokens))} عدد", callback_data="None-1"),
            Button(text="💎 توکن درخواستی:", callback_data="None-2"),
        )
        
        self.inline_keyboard.add_row(
            Button(text=f"{english_to_persian(number_formatter(amount))} تومان", callback_data="None-3"),
            Button("💰 قیمت کل:", callback_data="None-4"),
        )
        
        if discount_code:
            
            if discount_code.check_expiration():
                payment_text += "\n" + "❌ کد تخفیف منقضی شده است!"
            else:
                discount_per_token = token_settings.unit - (token_settings.unit * (discount_code.percent / 100))
                total_discount = amount * (discount_code.percent / 100)
                amount_with_discount = amount - total_discount
                
                payment_text += "\n" + f"تخفیف: *{english_to_persian(number_formatter(discount_code.percent))}* درصد"
                payment_text += "\n" + f"قیمت هر توکن با تخفیف: *{english_to_persian(number_formatter(discount_per_token))}* تومان"
                payment_text += "\n" + f"تخفیف کل: *{english_to_persian(number_formatter(total_discount))}* تومان"
                
                self.inline_keyboard.add_row(
                    Button(text=f"{english_to_persian(number_formatter(amount_with_discount))} تومان", callback_data="None-7"),
                    Button("💰 قیمت با تخفیف:", callback_data="None-8"),
                )
                
        self.inline_keyboard.add_row(
            Button(text='🔗 ساخت لینک پرداخت', callback_data=callback_data.encode(step=self.step+1)),
            
        )
        
        if not discount_code:
            self.inline_keyboard.add_row(
                Button(text='🎁 اعمال کد تخفیف', callback_data="dc_cnvstn"),
            )
        
        self.inline_keyboard.add_row(back, close)

        await self.save_conversation_usecase.execute(chat_id, callback_data, conversation.messages)
        
        return payment_text, self.inline_keyboard.create_markup()