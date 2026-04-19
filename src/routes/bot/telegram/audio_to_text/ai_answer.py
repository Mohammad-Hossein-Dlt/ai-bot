from telegram import Update
from telegram.ext import ContextTypes

from fast_depends import inject, Depends

from . import request_name
from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo

from src.infra.schemas.ai_client.ai_client import AiClient
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard

from src.routes.depends.repo_depend import cache_repo_depend, user_repo_depend, category_repo_depend, token_settings_repo_depend
from src.routes.depends.ai_depend import ai_client_depend
from src.routes.depends.inline_keyboard_depend import inline_keyboard_depend
from src.routes.depends.bot_platform_depend import bot_platform_depend

from src.models.schemas.bot.audio_to_text_request_model import AudioToTextRequestModel
from src.usecases.bot.audio_to_text.steps.choose_ai_platform import ChooseAiPlatform
from src.usecases.bot.audio_to_text.steps.choose_model import ChooseModel
from src.usecases.bot.audio_to_text.steps.request_summary import RequestSummary
from src.usecases.bot.audio_to_text.steps.produce import Produce
from src.usecases.bot.audio_to_text.cache import ProduceAudioCache

from io import BytesIO

@inject
async def request_steps(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    callback_data: CallbackDataRequest | None = None,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    token_settings_repo: ITokenSettingsRepo = Depends(token_settings_repo_depend),
    ai_client: AiClient = Depends(ai_client_depend),
    inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
    bot_platform: str = Depends(bot_platform_depend),
):
    
    start_point = callback_data is None
    
    chat_id = update.effective_user.id
      
    callback_data = callback_data or CallbackDataRequest(name=request_name, message_id=update.message.message_id)
    
    cache_usecase = ProduceAudioCache(
        cache_repo,
        user_repo,
        category_repo,
    )
    
    request: AudioToTextRequestModel = await cache_usecase.execute(chat_id, callback_data)
    
    if start_point:
        
        choose_ai_platform_usecase = ChooseAiPlatform(inline_keyboard)
        
        text, keyboard = choose_ai_platform_usecase.execute(callback_data)
                
        await update.effective_message.reply_text(
            text=text,
            reply_to_message_id=update.message.message_id,
            reply_markup=keyboard,
        )
        
    elif callback_data.step == ChooseAiPlatform.step:
        
        choose_ai_platform_usecase = ChooseAiPlatform(inline_keyboard)
        
        text, keyboard = choose_ai_platform_usecase.execute(callback_data)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )
                
    elif callback_data.step == ChooseModel.step:
        
        choose_ai_model_usecase = ChooseModel(
            category_repo,
            inline_keyboard,
        )
        
        text, keyboard = await choose_ai_model_usecase.execute(callback_data, request)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )
        
    elif callback_data.step == RequestSummary.step:

        request_summary_usecase = RequestSummary(
            cache_repo,
            user_repo,
            token_settings_repo,
            category_repo,
            inline_keyboard,
            bot_platform,
        )
        
        text, keyboard = await request_summary_usecase.execute(callback_data, request, chat_id)

        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )
        
    elif callback_data.step == Produce.step:
        
        file_name = update.message.document.file_name
        file = await update.message.document.get_file()
        
        audio = BytesIO()
        await file.download_to_memory(audio)
        audio.seek(0)
        
        produce_usecase = Produce(
            user_repo,
            token_settings_repo,
            category_repo,
            ai_client,
            bot_platform,
        )
        
        async for text, keyboard, content in produce_usecase.execute(request, str(chat_id), file_name, audio):
            
            if keyboard and content:
                await update.effective_message.reply_text(
                    content,
                    reply_markup=keyboard,
                )
            elif not content:
                await update.effective_message.reply_text(
                    text,
                    reply_markup=keyboard,
                )
            elif not keyboard:
                await update.effective_message.reply_text(
                    content,
                )
            else:
                await update.effective_message.reply_text(
                    text,
                )