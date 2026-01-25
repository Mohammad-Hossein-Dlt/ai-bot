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
# from bot_routers.add_credit import add_credit
from .show_profile import show_profile

from .produce_content import request_name as produce_content_request_name
from .produce_content.ai_answer import request_steps as produce_content_request_steps
from .produce_content.on_callback import on_callback as produce_content_callback
from .produce_content.enter_prompt import entry_point, enter_prompt

from .produce_image import request_name as produce_image_request_name
from .produce_image.ai_answer import request_steps as produce_image_request_steps
from .produce_image.on_callback import on_callback as produce_image_callback

from .produce_voice import request_name as produce_voice_request_name
from .produce_voice.ai_answer import request_steps as produce_voice_request_steps
from .produce_voice.on_callback import on_callback as produce_voice_callback

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
    
    if text == SHOW_PROFILE:
        await show_profile(update, context)
    # elif text == ADD_CREDIT:
    #     await add_credit(
    #         message,
    #         bot_client,
    #     )
    elif text == GUIDE:
        await guide(update, context)
    elif text == CREATE_ARTICLE:
        await produce_content_request_steps(
            update,
            context,
        )
    elif text == CREATE_IMAGE:
        await produce_image_request_steps(
            update,
            context,
        )
    elif text == CREATE_ARTICLE:
        await produce_voice_request_steps(
            update,
            context,
        )
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

def start_bot():
    # application = Application.builder().token(settings.BOT_TOKEN).post_init(on_startup).build()
    application = Application.builder().token(settings.BOT_TOKEN).post_init(on_startup).base_url("https://tapi.bale.ai/bot").build()
    # application = Application.builder().token(BOT_TOKEN).base_url("https://botapi.rubika.ir/v3/").build()
    
    enter_prompt_handler = ConversationHandler(
        entry_points=[
            # CallbackQueryHandler(callback=entry_point, pattern=request_pattern(produce_content_request_name + "cnvtion", **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=entry_point, pattern="conversation"),
        ],
        states={
            0: [
                MessageHandler(filters=filters.TEXT, callback=enter_prompt),
            ],
        },
        fallbacks=[],
    )
    
    application.add_handlers(
        [
            CommandHandler("start", start),
            enter_prompt_handler,
            MessageHandler(filters=None, callback=on_message),
            CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
            CallbackQueryHandler(callback=produce_content_callback, pattern=request_pattern(produce_content_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=produce_image_callback, pattern=request_pattern(produce_image_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=produce_voice_callback, pattern=request_pattern(produce_voice_request_name, **CallbackDataRequest.aliases)),
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
