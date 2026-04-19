from telegram import KeyboardButton, ReplyKeyboardMarkup

from raw_texts.raw_texts import (
    CONTENT_CREATION,
    TEXT_TO_IMAGE,
    TEXT_TO_AUDIO,
    AUDIO_TO_TEXT,
    PROFILE,
    ADD_CREDIT,
    PRICING,
    GUIDE,
    BACK
)

home_buttons = [
    [
        KeyboardButton(text=CONTENT_CREATION),
    ],
    [
        KeyboardButton(text=TEXT_TO_IMAGE),
        KeyboardButton(text=TEXT_TO_AUDIO),
        KeyboardButton(text=AUDIO_TO_TEXT),
    ],
    [
        KeyboardButton(text=PROFILE),
        KeyboardButton(text=ADD_CREDIT),
        KeyboardButton(text=PRICING),
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
