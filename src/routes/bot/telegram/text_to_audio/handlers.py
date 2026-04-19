from telegram.ext import MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from src.infra.utils.callback_data import request_pattern
from src.routes.bot.telegram.on_callback import on_callback
from .enter_prompt import entry_point, enter_prompt, back_from_conversation

text_to_audio_enter_prompt_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=entry_point, pattern="pv_cnvstn"),
    ],
    states={
        0: [
            MessageHandler(filters=filters.TEXT, callback=enter_prompt),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(callback=back_from_conversation, pattern="back_from_cnvstn"),
        CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
    ],
)