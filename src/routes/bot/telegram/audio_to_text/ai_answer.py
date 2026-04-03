from telegram import Update
from telegram.ext import ContextTypes

from fast_depends import inject, Depends

from . import request_name
from src.models.schemas.bot.callback_request import CallbackDataRequest
from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.routes.depends.repo_depend import cache_repo_depend, user_repo_depend, token_settings_repo_depend
from src.routes.depends.inline_keyboard_depend import inline_keyboard_depend
from src.routes.depends.gpt_depend import gpt_client_depend
from src.models.schemas.bot.text_to_audio_request_model import TextToAudioRequestModel
from src.usecases.bot.audio_to_text.steps.choose_ai import ChooseAiPlatform
from src.usecases.bot.audio_to_text.steps.request_summary import RequestSummary
from src.usecases.bot.audio_to_text.steps.produce import Produce
from src.usecases.bot.audio_to_text.cache import ProduceAudioCache

from openai import OpenAI
from io import BytesIO

ai_platforms = ["gemini", "chat-gpt"]

@inject
async def request_steps(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    callback_data: CallbackDataRequest | None = None,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    token_settings_repo: ITokenSettingsRepo = Depends(token_settings_repo_depend),
    inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
    gpt_client: OpenAI = Depends(gpt_client_depend),
):
    
    start_point = callback_data is None
    
    chat_id = update.effective_user.id
      
    callback_data = callback_data or CallbackDataRequest(name=request_name, message_id=update.message.message_id)
    cache_usecase = ProduceAudioCache(user_repo, cache_repo, ai_platforms)
    request: TextToAudioRequestModel = await cache_usecase.execute(chat_id, callback_data)
    
    if start_point:
        
        prompt_usecase = ChooseAiPlatform(ai_platforms, inline_keyboard)
        text, keyboard = prompt_usecase.execute(callback_data)
                
        await update.effective_message.reply_text(
            text=text,
            reply_to_message_id=update.message.message_id,
            reply_markup=keyboard,
        )
        
    elif callback_data.step == ChooseAiPlatform.step:
        
        prompt_usecase = ChooseAiPlatform(ai_platforms, inline_keyboard)
        text, keyboard = prompt_usecase.execute(callback_data)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )
        
    elif callback_data.step == RequestSummary.step:

        request_summary = RequestSummary(user_repo, token_settings_repo, cache_repo, inline_keyboard)
        text, keyboard = await request_summary.execute(chat_id, request, callback_data)

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
        
        produce_usecase = Produce(user_repo, token_settings_repo, cache_repo, gpt_client, inline_keyboard)
        async for text, keyboard, content in produce_usecase.execute(str(chat_id), file_name, audio, request):
            
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