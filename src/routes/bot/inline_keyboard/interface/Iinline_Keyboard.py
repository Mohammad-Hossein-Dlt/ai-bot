from dataclasses import dataclass

@dataclass
class Button:
    text: str
    callback_data: str
    is_link: bool = False

class IInlineKeyboard:

    def create_button(
        button_data: Button,
    ):
        raise NotImplementedError

    def add_button(
        button_data: Button,
    ):
        raise NotImplementedError

    def add_column(
        *args: Button | None,
    ):
        raise NotImplementedError
    
    def add_row(
        *args: Button | None,
    ):
        raise NotImplementedError
    
    def create_markup():
        raise NotImplementedError