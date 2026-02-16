from telegram import Update, InputFile
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
from src.models.schemas.bot.request_model import RequestModel
from src.usecases.bot.produce_content.steps.choose_prompt import ChoosePrompt
from src.usecases.bot.produce_content.steps.choose_words_number import ChooseWordsNumber
from src.usecases.bot.produce_content.steps.choose_tones import ChooseTones
from src.usecases.bot.produce_content.steps.request_summary import RequestSummary
from src.usecases.bot.produce_content.steps.produce import Produce
from src.usecases.bot.produce_content.cache import ProduceContentCache

from prompts.prompt_list import prompts_titles, tones, words_number
from openai import OpenAI

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
    cache_usecase = ProduceContentCache(user_repo, cache_repo, prompts_titles, words_number, tones)
    request: RequestModel = await cache_usecase.execute(chat_id, callback_data)
    
    if start_point:
        
        prompt_usecase = ChoosePrompt(prompts_titles, inline_keyboard)
        text, keyboard = prompt_usecase.execute(callback_data)
                
        await update.effective_message.reply_text(
            text=text,
            reply_to_message_id=update.message.message_id,
            reply_markup=keyboard,
        )
        
    elif callback_data.step == ChoosePrompt.step:
        
        prompt_usecase = ChoosePrompt(prompts_titles, inline_keyboard)
        text, keyboard = prompt_usecase.execute(callback_data)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )

    elif callback_data.step == ChooseWordsNumber.step:
        
        words_number_usecase = ChooseWordsNumber(words_number, inline_keyboard)
        text, keyboard = words_number_usecase.execute(callback_data)
        
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )

    elif callback_data.step == ChooseTones.step:

        tones_usecase = ChooseTones(tones, inline_keyboard)
        text, keyboard = tones_usecase.execute(request, callback_data)

        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )

    elif callback_data.step == RequestSummary.step:

        produce_usecase = RequestSummary(user_repo, token_settings_repo, cache_repo, inline_keyboard)
        text, keyboard = await produce_usecase.execute(chat_id, request, callback_data)

        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )

    elif callback_data.step == Produce.step:

        produce_usecase = Produce(user_repo, token_settings_repo, cache_repo, gpt_client, inline_keyboard)
        async for text, keyboard, file in produce_usecase.execute(str(chat_id), request):
            
            if keyboard and file:
                await update.effective_message.reply_document(
                    document=InputFile(
                        file.read(),
                        filename='document.pdf'
                    ),
                    caption=text,
                    reply_markup=keyboard,
                )
            elif not file:
                await update.effective_message.reply_text(
                    text,
                    reply_markup=keyboard,
                )
            elif not keyboard:
                await update.effective_message.reply_document(
                    document=InputFile(
                        file.read(),
                        file_name='document.pdf'
                    ),
                    caption=text,
                )
            else:
                await update.effective_message.reply_text(
                    text,
                )
