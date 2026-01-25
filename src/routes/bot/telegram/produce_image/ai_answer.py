from telegram import Update, InputFile, InputMediaPhoto
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

from openai import OpenAI

import base64

@inject
async def request_steps(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    # callback_data: CallbackDataRequest | None = None,
    # cache_repo: ICacheRepo = Depends(cache_repo_depend),
    # user_repo: IUserRepo = Depends(user_repo_depend),
    # token_settings_repo: ITokenSettingsRepo = Depends(token_settings_repo_depend),
    # inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
    gpt_client: OpenAI = Depends(gpt_client_depend),
):
    
    print("////")
    
    # start_point = callback_data is None
    
    # chat_id = update.effective_user.id
    
    # callback_data = callback_data or CallbackDataRequest(name=request_name, message_id=update.message.message_id)    
    # cache_usecase = ProduceContentCache(user_repo, cache_repo, prompts_titles, words_number, tones)
    # request: RequestModel = await cache_usecase.execute(chat_id, callback_data)
    
    prompt = "یک ربات ایرانی در حال برنامه نویسی، سبک کارتونی"

    result = gpt_client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0]
    print(image_base64)
    print(image_base64.url)
    image_bytes = base64.b64decode(image_base64.b64_json)
    
    await update.effective_message.reply_media_group(
        [
            InputMediaPhoto(
                InputFile(
                    image_bytes,
                ),
            ),  
        ],
    )
    