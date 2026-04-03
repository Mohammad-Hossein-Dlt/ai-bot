from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters

from fast_depends import inject, Depends

from src.infra.context.context_manager import AppContextManager
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.account_model import AccountModel
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.settings.settings import settings
from src.infra.utils.callback_data import request_pattern, request_decoder
from src.models.schemas.bot.callback_request import CallbackDataRequest

from .general_buttons import home_markup

from .produce_content import request_name as produce_content_request_name
from .produce_content.ai_answer import request_steps as produce_content_request_steps
from .produce_content.on_callback import on_callback as produce_content_callback
from .produce_content.enter_prompt import (
    entry_point as produce_content_entry_point,
    enter_prompt as produce_content_enter_prompt,
    back_from_conversation as produce_content_back_from_conversation
)

from .text_to_image import request_name as text_to_image_request_name
from .text_to_image.ai_answer import request_steps as text_to_image_request_steps
from .text_to_image.on_callback import on_callback as text_to_image_callback
from .text_to_image.enter_prompt import (
    entry_point as text_to_image_entry_point,
    enter_prompt as text_to_image_enter_prompt,
    back_from_conversation as text_to_image_back_from_conversation
)

from .text_to_audio import request_name as text_to_audio_request_name
from .text_to_audio.ai_answer import request_steps as text_to_audio_request_steps
from .text_to_audio.on_callback import on_callback as text_to_audio_callback
from .text_to_audio.enter_prompt import (
    entry_point as text_to_audio_entry_point,
    enter_prompt as text_to_audio_enter_prompt,
    back_from_conversation as text_to_audio_back_from_conversation
)

from .audio_to_text import request_name as audio_to_text_request_name
from .audio_to_text.ai_answer import request_steps as audio_to_text_request_steps
from .audio_to_text.on_callback import on_callback as audio_to_text_callback
from .audio_to_text.enter_prompt import (
    entry_point as audio_to_text_entry_point,
    enter_prompt as audio_to_text_enter_prompt,
    back_from_conversation as audio_to_text_back_from_conversation
)

from .show_profile import show_profile

from .add_credit import request_name as add_credit_request_name
from .add_credit.add_credit import request_steps as add_credit_request_steps
from .add_credit.on_callback import on_callback as add_credit_callback
from .add_credit.enter_token import (
    entry_point as add_credit_entry_point,
    enter_token,
    back_from_conversation as add_credit_back_from_conversation,
)

from .guide import guide

from raw_texts.raw_texts import *
from src.infra.exceptions.exceptions import EntityNotFoundError

async def on_startup(app: Application):
    await AppContextManager.lazy_init_context()
    print("Bot is Running...")

@inject
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    
    user_id = update.effective_user.id
            
    try:
        await user_repo.get_by_chat_id(user_id)
        await update.message.reply_text(WELCOME, reply_markup=home_markup)
    except EntityNotFoundError:
        platform_accounts = [
            AccountModel(chat_id=str(user_id)),
        ]
        user = UserModel(platform_accounts=platform_accounts)
        await user_repo.create(user) 
        await update.message.reply_text(WELCOME, reply_markup=home_markup)

async def on_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    
    text = update.effective_message.text
    
    if text == CREATE_ARTICLE:
        await produce_content_request_steps(update, context)
    elif text == CREATE_IMAGE:
        await text_to_image_request_steps(update, context)
    elif text == TEXT_TO_AUDIO:
        await text_to_audio_request_steps(update, context)
    elif text == AUDIO_TO_TEXT:
        await audio_to_text_request_steps(update, context)
    elif text == SHOW_PROFILE:
        await show_profile(update, context)
    elif text == ADD_CREDIT:
        await add_credit_request_steps(update, context)
    elif text == GUIDE:
        await guide(update, context)
    elif text == BACK:
        await update.message.reply_text(
            text=RESTART,
            reply_markup=home_markup,
        )

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

def start_bot():
    # application = Application.builder().token(settings.BOT_TOKEN).post_init(on_startup).build()
    application = Application.builder().token(settings.BOT_TOKEN).post_init(on_startup).base_url("https://tapi.bale.ai/bot").base_file_url("https://tapi.bale.ai/file/bot").build()
    # application = Application.builder().token(BOT_TOKEN).base_url("https://botapi.rubika.ir/v3/").build()
    
    produce_content_enter_prompt_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(callback=produce_content_entry_point, pattern="pc_cnvstn"),
        ],
        states={
            0: [
                MessageHandler(filters=filters.TEXT, callback=produce_content_enter_prompt),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(callback=produce_content_back_from_conversation, pattern="back_from_cnvstn"),
            CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
        ],
    )
    
    text_to_image_enter_prompt_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(callback=text_to_image_entry_point, pattern="pi_cnvstn"),
        ],
        states={
            0: [
                MessageHandler(filters=filters.TEXT, callback=text_to_image_enter_prompt),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(callback=text_to_image_back_from_conversation, pattern="back_from_cnvstn"),
            CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
        ],
    )
        
    text_to_audio_enter_prompt_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(callback=text_to_audio_entry_point, pattern="pv_cnvstn"),
        ],
        states={
            0: [
                MessageHandler(filters=filters.TEXT, callback=text_to_audio_enter_prompt),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(callback=text_to_audio_back_from_conversation, pattern="back_from_cnvstn"),
            CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
        ],
    )
    
    audio_to_text_enter_prompt_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(callback=audio_to_text_entry_point, pattern="vt_cnvstn"),
        ],
        states={
            0: [
                MessageHandler(filters=filters.Document.AUDIO, callback=audio_to_text_enter_prompt),
            ],
        },
        fallbacks=[
            CallbackQueryHandler(callback=audio_to_text_back_from_conversation, pattern="back_from_cnvstn"),
            CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
        ],
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
    
    application.add_handlers(
        [
            CommandHandler("start", start),
            produce_content_enter_prompt_handler,
            text_to_image_enter_prompt_handler,
            text_to_audio_enter_prompt_handler,
            audio_to_text_enter_prompt_handler,
            add_credit_handler,
            MessageHandler(filters=None, callback=on_message),
            CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
            CallbackQueryHandler(callback=produce_content_callback, pattern=request_pattern(produce_content_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=text_to_image_callback, pattern=request_pattern(text_to_image_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=text_to_audio_callback, pattern=request_pattern(text_to_audio_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=audio_to_text_callback, pattern=request_pattern(audio_to_text_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=add_credit_callback, pattern=request_pattern(add_credit_request_name, **CallbackDataRequest.aliases)),
        ],
    )
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    start_bot()

'''
cpcpcs:10p:10o:ttttti:1000t:50768658977200r:1000000000

cps:10p:10o:tti:1000r:1000000
cps:1p:1o:tti:1000r:1000000000
nnnnns:10p:10o:nnnnni:1000m:1000000000
'''
