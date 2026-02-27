from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import Button, IInlineKeyboard
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

class BaleInlineKeyboard(IInlineKeyboard):
    
    def __init__(
        self,
    ):
        self.buttons = []

    def create_button(
        self,
        button_data: Button,
    ):        
        if button_data.is_link:
            return InlineKeyboardButton(button_data.text, url=button_data.callback_data)
        
        return InlineKeyboardButton(button_data.text, callback_data=button_data.callback_data)
        
    def add_button(
        self,
        button_data: Button,
    ):
        self.buttons.append(
            [
                self.create_button(button_data),
            ],
        )

    def add_column(
        self,
        *args: Button | None,
    ):
        for var in args:
            if var:
                self.add_button(var)
                    
    def add_row(
        self,
        *args: Button | None,
    ):
        row = []
        for var in args:
            if var:
                row.append(
                    self.create_button(var),
                )
        
        if row:
            row.reverse()
            self.buttons.append(row)

    def create_markup(
        self,
    ):  
        return InlineKeyboardMarkup(self.buttons)