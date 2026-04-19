from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from src.infra.utils.callback_data import request_pattern, request_decoder

async def on_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    
    query = update.callback_query
    
    await query.answer()
    
    try:
        pattern = request_pattern(close="id")
        message_id = request_decoder(query.data, pattern).get("id", None)
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=update.effective_message.message_id,
        )
        await context.bot.delete_message(
            chat_id=update.effective_chat.id,
            message_id=message_id,
        )
    except: ...
    
    return ConversationHandler.END