from telegram import KeyboardButton, ReplyKeyboardMarkup

from raw_texts.raw_texts import (
    CREATE_ARTICLE,
    CREATE_IMAGE,
    CREATE_VOICE,
    SHOW_PROFILE,
    ADD_CREDIT,
    GUIDE,
    BACK
)

home_buttons = [
    [
        KeyboardButton(text=CREATE_ARTICLE),
    ],
    [
        KeyboardButton(text=CREATE_IMAGE),
        KeyboardButton(text=CREATE_VOICE),
    ],
    [
        KeyboardButton(text=SHOW_PROFILE),
        KeyboardButton(text=ADD_CREDIT),
    ],
    [
        KeyboardButton(text=GUIDE),
    ],
]

home_markup = ReplyKeyboardMarkup(keyboard=home_buttons, resize_keyboard=True)

back_markup = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(BACK),
        ],
    ],
    resize_keyboard=True,
)
