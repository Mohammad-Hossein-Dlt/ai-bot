from src.infra.context.app_context import AppContext
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.routes.bot.inline_keyboard.implementations.telegram_inline_Keyboard import TelegramInlineKeyboard
from src.routes.bot.inline_keyboard.implementations.bale_inline_Keyboard import BaleInlineKeyboard

def inline_keyboard_depend() -> IInlineKeyboard:
    platform = AppContext.bot_platform
    if platform == "telegram":
        return TelegramInlineKeyboard()   
    elif platform == "bale":
        return BaleInlineKeyboard()
    elif platform == "rubika":
        return TelegramInlineKeyboard()