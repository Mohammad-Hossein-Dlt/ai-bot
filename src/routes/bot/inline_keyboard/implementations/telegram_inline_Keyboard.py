from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class TelegramInlineKeyboard(IInlineKeyboard):
    
    def __init__(
        self,
    ):
        self.buttons = []

    def create_button(
        self,
        text: str,
        callback_data: str,
    ):        
        return InlineKeyboardButton(text, callback_data=callback_data)
        
    def add_button(
        self,
        text: str,
        callback_data: str,
    ):
        self.buttons.append(
            [
                self.create_button(text, callback_data),
            ],
        )

    def add_column(
        self,
        *args: dict[str, str] | None,
    ):
        for var in args:
            if var:
                for key, value in var.items():
                    self.add_button(key, value)
                    
    def add_row(
        self,
        *args: dict[str, str] | None,
    ):
        row = []
        for var in args:
            if var:
                for key, value in var.items():
                    row.append(
                        self.create_button(key, value),
                    )
        
        if row:
            self.buttons.append(row)

    def create_markup(
        self,
    ):  
        return InlineKeyboardMarkup(self.buttons)