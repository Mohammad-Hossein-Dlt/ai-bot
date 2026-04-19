from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from fast_depends import inject, Depends

from .add_credit import request_steps

from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Icache import ICacheRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.routes.depends.repo_depend import user_repo_depend, cache_repo_depend
from src.routes.depends.inline_keyboard_depend import inline_keyboard_depend
from src.usecases.bot.save_conversation import SaveConversation
from src.usecases.bot.get_conversation import GetConversation
from src.models.schemas.bot.conversation_model import ConversationModel
from src.usecases.bot.add_credit.steps.enter_discount_code import EnterDiscountCode

@inject
async def entry_point(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
) -> int:
    
    chat_id = update.effective_user.id

    get_conversation_usecase = GetConversation(cache_repo, user_repo)
    conversation = await get_conversation_usecase.execute(chat_id)

    enter_token_usecase = EnterDiscountCode(inline_keyboard)
    text, keyboard = await enter_token_usecase.execute(conversation.callback_data)
    
    await update.effective_message.edit_text(
        text=text,
        reply_markup=keyboard,
    )
    
    return 0

@inject
async def back_from_conversation(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> int:
    
    chat_id = update.effective_user.id
    
    get_conversation_usecase = GetConversation(cache_repo, user_repo)
    conversation = await get_conversation_usecase.execute(chat_id)
            
    await request_steps(
        update,
        context,
        conversation.callback_data,
    )
    
    return ConversationHandler.END

@inject
async def enter_discount_code(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> int:
    
    chat_id = update.effective_user.id
    discount_code = update.effective_message.text

    get_conversation_usecase = GetConversation(cache_repo, user_repo)
    conversation = await get_conversation_usecase.execute(chat_id)
    
    messages = conversation.messages
    messages.update({"discount_code": discount_code})
    
    save_conversation_usecase = SaveConversation(cache_repo, user_repo)
    conversation: ConversationModel = await save_conversation_usecase.execute(
        chat_id,
        messages=messages,
    )
    
    callback_data = conversation.callback_data
    
    await request_steps(
        update,
        context,
        callback_data,
    )
    
    return ConversationHandler.END