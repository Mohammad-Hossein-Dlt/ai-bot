numbers = {
    '۰': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9',
}


def persian_to_english(value: str) -> str:
    for persian, english in numbers.items():
        value = value.replace(persian, english)

    return value


def english_to_persian(value: str) -> str:
    for persian, english in numbers.items():
        value = value.replace(english, persian)

    return value


def number_formatter(value: int | float) -> str:
    
    if isinstance(value, float):
        if value.is_integer():
            # to remove .0
            return '{:,}'.format(int(value))
    
    return '{:,}'.format(value)
