from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from fast_depends import inject, Depends

from .ai_answer import request_steps

from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Icache import ICacheRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard
from src.routes.depends.repo_depend import user_repo_depend, cache_repo_depend
from src.routes.depends.inline_keyboard_depend import inline_keyboard_depend
from src.usecases.bot.save_conversation import SaveConversation
from src.usecases.bot.get_conversation import GetConversation
from src.models.schemas.bot.conversation_model import ConversationModel
from src.usecases.bot.text_to_image.steps.enter_prompt import EnterPrompt

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

    enter_prompt_usecase = EnterPrompt(inline_keyboard)
    text, keyboard = await enter_prompt_usecase.execute(conversation.callback_data)
    
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
    
    callback_data = conversation.callback_data
    
    await request_steps(
        update,
        context,
        callback_data,
    )
    
    return ConversationHandler.END

@inject
async def enter_prompt(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> int:
    
    chat_id = update.effective_user.id
    prompt = update.effective_message.text

    save_conversation_usecase = SaveConversation(cache_repo, user_repo)
    conversation: ConversationModel = await save_conversation_usecase.execute(chat_id, messages={"prompt": prompt})
    
    callback_data = conversation.callback_data
    
    callback_data.step += 1
    callback_data.page = 0
    
    await request_steps(
        update,
        context,
        callback_data,
    )
    
    return ConversationHandler.END