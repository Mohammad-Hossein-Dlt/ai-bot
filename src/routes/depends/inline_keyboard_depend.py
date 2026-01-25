from src.infra.context.app_context import AppContext
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.routes.bot.inline_keyboard.implementations.telegram_inline_Keyboard import TelegramInlineKeyboard
from src.routes.bot.inline_keyboard.implementations.bale_inline_Keyboard import BaleInlineKeyboard

def inline_keyboard_depend() -> IInlineKeyboard:
    platform = AppContext.platform
    if platform == "Telegram_bot":
        return TelegramInlineKeyboard()   
    elif platform == "Bale_bot":
        return BaleInlineKeyboard()
    elif platform == "Rubika_bot":
        return TelegramInlineKeyboard()