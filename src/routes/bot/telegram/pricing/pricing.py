from telegram import Update
from telegram.ext import ContextTypes

from fast_depends import inject, Depends

from . import request_name
from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard

from src.routes.depends.repo_depend import cache_repo_depend, user_repo_depend, category_repo_depend
from src.routes.depends.inline_keyboard_depend import inline_keyboard_depend

from src.models.schemas.bot.pricing import PricingRequestModel
from src.usecases.bot.pricing.cache import PricingCache
from src.usecases.bot.pricing.steps.choose_ai_action_type import ChooseAiActionType
from src.usecases.bot.pricing.steps.categories_price_amount import CategoriesPriceAmount

from raw_texts.raw_texts import CONTENT_CREATION, TEXT_TO_IMAGE, TEXT_TO_AUDIO, AUDIO_TO_TEXT

ai_action_type_fa = [
    CONTENT_CREATION,
    TEXT_TO_IMAGE,
    TEXT_TO_AUDIO,
    AUDIO_TO_TEXT
]

@inject
async def request_steps(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    callback_data: CallbackDataRequest | None = None,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
    inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
):
    
    start_point = callback_data is None
    
    chat_id = update.effective_user.id
    
    callback_data = callback_data or CallbackDataRequest(name=request_name, message_id=update.message.message_id)
    
    cache_usecase = PricingCache(
        cache_repo,
        user_repo,
        ai_action_type_fa,
    )
    
    request: PricingRequestModel = await cache_usecase.execute(chat_id, callback_data)
    
    if start_point:
                
        choose_ai_actions_type_usecase = ChooseAiActionType(
            ai_action_type_fa,
            inline_keyboard,
        )
        
        text, keyboard = choose_ai_actions_type_usecase.execute(callback_data)
                
        await update.effective_message.reply_text(
            text=text,
            reply_markup=keyboard,
        )
             
    elif callback_data.step == ChooseAiActionType.step:
                
        choose_ai_actions_type_usecase = ChooseAiActionType(
            ai_action_type_fa,
            inline_keyboard,
        )
        
        text, keyboard = choose_ai_actions_type_usecase.execute(callback_data)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )
        
    elif callback_data.step == CategoriesPriceAmount.step:
                
        categories_price_amount_usecase = CategoriesPriceAmount(
            category_repo,
            inline_keyboard,
        )
        
        text, keyboard = await categories_price_amount_usecase.execute(callback_data, request)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )