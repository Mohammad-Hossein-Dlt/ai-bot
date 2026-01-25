
class IInlineKeyboard:

    def create_button(
        text: str,
        callback_data: str,
    ):
        raise NotImplementedError

    def add_button(
        text: str,
        callback_data: str,
    ):
        raise NotImplementedError

    def add_column(
        *args: dict[str, str] | None,
    ):
        raise NotImplementedError
    
    def add_row(
        *args: dict[str, str] | None,
    ):
        raise NotImplementedError
    
    def create_markup():
        raise NotImplementedError