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
from src.models.schemas.bot.produce_content_request_model import ProduceContentRequestModel

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

    result = gpt_client.chat.completions.create(
        model="gemini-3-pro-image-preview",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        modalities=["image", "text"],
        extra_body={
            "generationConfig": {"imageConfig": {"aspectRatio": "16:9", "imageSize": "2K"}}
        },
    )
    
    if hasattr(result.choices[0].message, "images"):
        images = getattr(result.choices[0].message, "images")
        for img in images:
            if isinstance(img, dict) and "image_url" in img:
                # img_url = img["image_url"]
                # if isinstance(img_url, dict):
                #     print(list(img_url.keys()))
                # print(f"Image URL: {img["image_url"]["url"][:100]}...")
                
                # await update.effective_message.reply_text(base64.b64decode(img["image_url"]["url"]))
                image_bytes = base64.urlsafe_b64decode(img["image_url"]["url"])
                print(image_bytes.decode())
                with open("img.txt", "wb") as f:
                    # f.write(img["image_url"]["url"])
                    f.write(image_bytes)
                
                await update.effective_message.reply_media_group(
                    [
                        InputMediaPhoto(
                            InputFile(
                                image_bytes,
                            ),
                        ),  
                    ],
                )
    else:
        await update.effective_message.reply_text("None")
            
    # image_bytes = base64.b64decode(image_base64.b64_json)
    
    # await update.effective_message.reply_media_group(
    #     [
    #         InputMediaPhoto(
    #             InputFile(
    #                 image_bytes,
    #             ),
    #         ),  
    #     ],
    # )