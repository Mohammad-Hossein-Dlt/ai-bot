from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.models.schemas.bot.callback_request import CallbackDataRequest
from typing import ClassVar
from raw_texts.raw_texts import (
    BACK,
    CLOSE_PANEL,
)
from src.infra.utils.number_converter import english_to_persian, persian_to_english, number_formatter

class EnterToken:
    
    # step: ClassVar[int] = 1
    
    def __init__(
        self,
        token_settings_repo: ITokenSettingsRepo,
        inline_keyboard: IInlineKeyboard,
    ):
        self.token_settings_repo = token_settings_repo
        self.inline_keyboard = inline_keyboard
            
    async def execute(
        self,
        callback_data: CallbackDataRequest,
    ):
        
        token_settings: TokenSettingsModel = await self.token_settings_repo.get()

        max_amount_formatted = english_to_persian(number_formatter(token_settings.max_tokens))
        min_amount_formatted = english_to_persian(number_formatter(token_settings.min_tokens))

        enter_tokens = 'تعداد توکنی که میخواهید کیف پولتان را شارژ کنید، وارد کنید.'
        tokens_range = 'از تعداد min عدد تا تعداد max عدد، میتوانید توکن های کیف پولتان را شارژ کنید.'
        tokens_range = tokens_range.replace('min', min_amount_formatted).replace('max', max_amount_formatted)
        token_unit = 'قیمت هر واحد توکن unit ريال است'
        token_unit = token_unit.replace("unit", english_to_persian(number_formatter(token_settings.unit)))
        
        self.inline_keyboard.add_row(
            {BACK: "back_from_conversation"},
            {CLOSE_PANEL: f"close:{callback_data.message_id}"},
        )
        
        return f'{enter_tokens}\n{tokens_range}\n{token_unit}', self.inline_keyboard.create_markup()