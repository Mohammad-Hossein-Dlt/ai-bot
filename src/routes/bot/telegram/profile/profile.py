from telegram import Update
from telegram.ext import ContextTypes

from fast_depends import inject, Depends

from . import request_name
from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard

from src.routes.depends.repo_depend import user_repo_depend
from src.routes.depends.inline_keyboard_depend import inline_keyboard_depend

from src.usecases.bot.profile.steps.main_menu import MainMenu

@inject
async def request_steps(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    callback_data: CallbackDataRequest | None = None,
    user_repo: IUserRepo = Depends(user_repo_depend),
    inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
):
    
    start_point = callback_data is None
    
    chat_id = update.effective_user.id
    
    callback_data = callback_data or CallbackDataRequest(name=request_name, message_id=update.message.message_id)
    
    if start_point:
                
        main_menu_usecase = MainMenu(
            user_repo,
            inline_keyboard,
        )
        
        text, keyboard = await main_menu_usecase.execute(callback_data, chat_id)
                
        await update.effective_message.reply_text(
            text=text,
            reply_markup=keyboard,
        )
             
    elif callback_data.step == MainMenu.step:
                
        main_menu_usecase = MainMenu(
            user_repo,
            inline_keyboard,
        )
        
        text, keyboard = await main_menu_usecase.execute(callback_data, chat_id)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )