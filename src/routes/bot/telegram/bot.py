from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler

from fast_depends import inject, Depends

from src.infra.context.context_manager import AppContextManager
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.account_model import AccountModel
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.routes.depends.bot_platform_depend import bot_platform_depend
from src.infra.settings.settings import settings
from src.infra.utils.callback_data import request_pattern
from src.models.schemas.bot.callback_request import CallbackDataRequest

from .buttons import home_markup

from .on_message import on_message
from .on_callback import on_callback

from .content_creation import request_name as content_creation_request_name
from .content_creation.on_callback import on_callback as content_creation_on_callback
from .content_creation.handlers import content_creation_enter_prompt_handler

from .text_to_image import request_name as text_to_image_request_name
from .text_to_image.on_callback import on_callback as text_to_image_on_callback
from .text_to_image.handlers import text_to_image_enter_prompt_handler

from .text_to_audio import request_name as text_to_audio_request_name
from .text_to_audio.on_callback import on_callback as text_to_audio_on_callback
from .text_to_audio.handlers import text_to_audio_enter_prompt_handler

from .audio_to_text import request_name as audio_to_text_request_name
from .audio_to_text.on_callback import on_callback as audio_to_text_on_callback
from .audio_to_text.handlers import audio_to_text_enter_prompt_handler

from .add_credit import request_name as add_credit_request_name
from .add_credit.on_callback import on_callback as add_credit_on_callback
from .add_credit.handlers import add_credit_handler, discount_code_handler

from .pricing import request_name as pricing_request_name
from .pricing.on_callback import on_callback as pricing_on_callback

from src.infra.exceptions.exceptions import EntityNotFoundError

from raw_texts.raw_texts import WELCOME

async def on_startup(app: Application):
    await AppContextManager.lazy_init_context()
    print("Bot is Running...")

@inject
async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_repo: IUserRepo = Depends(user_repo_depend),
    bot_platform: str = Depends(bot_platform_depend),
):
    
    chat_id = update.effective_user.id
            
    try:
        await user_repo.get_by_chat_id(chat_id)
        await update.message.reply_text(WELCOME, reply_markup=home_markup)
    except EntityNotFoundError:
        user = UserModel(
            platform_accounts=AccountModel(
                chat_id=str(chat_id),
                platform=bot_platform,
            ),
        )
        await user_repo.create(user) 
        await update.message.reply_text(WELCOME, reply_markup=home_markup)


def start_bot():
    
    application = Application.builder().token(
        settings.BOT_TOKEN
    ).post_init(
        on_startup
    ).base_url(
        "https://tapi.bale.ai/bot"
    ).base_file_url(
        "https://tapi.bale.ai/file/bot"
    ).build()
    
    # application = Application.builder().token(settings.BOT_TOKEN).post_init(on_startup).build()
    # application = Application.builder().token(BOT_TOKEN).base_url("https://botapi.rubika.ir/v3/").build()
        
    
    application.add_handlers(
        [
            CommandHandler("start", start),
            content_creation_enter_prompt_handler,
            text_to_image_enter_prompt_handler,
            text_to_audio_enter_prompt_handler,
            audio_to_text_enter_prompt_handler,
            add_credit_handler,
            discount_code_handler,
            MessageHandler(filters=None, callback=on_message),
            CallbackQueryHandler(callback=on_callback, pattern=request_pattern(close="id")),
            CallbackQueryHandler(callback=content_creation_on_callback, pattern=request_pattern(content_creation_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=text_to_image_on_callback, pattern=request_pattern(text_to_image_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=text_to_audio_on_callback, pattern=request_pattern(text_to_audio_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=audio_to_text_on_callback, pattern=request_pattern(audio_to_text_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=add_credit_on_callback, pattern=request_pattern(add_credit_request_name, **CallbackDataRequest.aliases)),
            CallbackQueryHandler(callback=pricing_on_callback, pattern=request_pattern(pricing_request_name, **CallbackDataRequest.aliases)),
        ],
    )
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    start_bot()