from telegram import Update
from telegram.ext import ContextTypes
from . import request_name
from src.infra.utils.callback_data import request_pattern, request_decoder
from src.models.schemas.bot.callback_request import CallbackDataRequest
from .ai_answer import request_steps

async def on_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()
    
    pattern = request_pattern(request_name, **CallbackDataRequest.aliases)
    decoded = request_decoder(query.data, pattern)
    callback_data = CallbackDataRequest.model_validate(decoded)
        
    await request_steps(
        update,
        context,
        callback_data,
    )