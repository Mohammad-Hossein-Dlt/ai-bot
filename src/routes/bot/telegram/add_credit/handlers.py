from telegram.ext import MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from src.infra.utils.callback_data import request_pattern
from src.routes.bot.telegram.on_callback import on_callback
from .enter_token import (
    entry_point as add_credit_entry_point,
    enter_token,
    back_from_conversation as add_credit_back_from_conversation,
)
from .enter_discount_code import (
    entry_point as discount_code_entry_point,
    enter_discount_code,
    back_from_conversation as discount_code_back_from_conversation,
)

add_credit_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=add_credit_entry_point, pattern="ac_cnvstn"),
    ],
    states={
        0: [
            MessageHandler(filters=filters.TEXT, callback=enter_token),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(callback=add_credit_back_from_conversation, pattern="back_from_cnvstn"),
        CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
    ],
)
    
discount_code_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=discount_code_entry_point, pattern="dc_cnvstn"),
    ],
    states={
        0: [
            MessageHandler(filters=filters.TEXT, callback=enter_discount_code),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(callback=discount_code_back_from_conversation, pattern="back_from_cnvstn"),
        CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
    ],
)