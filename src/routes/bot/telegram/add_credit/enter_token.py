from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from fast_depends import inject, Depends

from .add_credit import request_steps

from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.routes.depends.repo_depend import token_settings_repo_depend, user_repo_depend, cache_repo_depend
from src.routes.depends.inline_keyboard_depend import inline_keyboard_depend
from src.usecases.bot.save_conversation import SaveConversation
from src.usecases.bot.get_conversation import GetConversation
from src.models.schemas.bot.conversation_model import ConversationModel
from src.usecases.bot.add_credit.steps.enter_token import EnterToken

@inject
async def entry_point(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    token_settings_repo: ITokenSettingsRepo = Depends(token_settings_repo_depend),
    inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
) -> int:
    
    chat_id = update.effective_user.id

    get_conversation_usecase = GetConversation(cache_repo, user_repo)
    conversation = await get_conversation_usecase.execute(chat_id)

    enter_token_usecase = EnterToken(token_settings_repo, inline_keyboard)
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
async def enter_token(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> int:
    
    chat_id = update.effective_user.id
    tokens = update.effective_message.text

    get_conversation_usecase = GetConversation(cache_repo, user_repo)
    conversation = await get_conversation_usecase.execute(chat_id)
    
    messages = conversation.messages
    messages.update({"tokens": tokens})

    save_conversation_usecase = SaveConversation(cache_repo, user_repo)
    conversation: ConversationModel = await save_conversation_usecase.execute(chat_id, messages=messages)
    
    callback_data = conversation.callback_data
    
    callback_data.step += 1
    callback_data.page = 0
    
    await request_steps(
        update,
        context,
        callback_data,
    )
    
    return ConversationHandler.END