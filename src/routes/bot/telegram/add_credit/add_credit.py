from telegram import Update
from telegram.ext import ContextTypes

from fast_depends import inject, Depends

from . import request_name
from src.models.schemas.bot.callback_request import CallbackDataRequest

from src.repo.interface.Icache import ICacheRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.routes.bot.inline_keyboard.interface.Iinline_Keyboard import IInlineKeyboard

from src.routes.depends.repo_depend import cache_repo_depend, user_repo_depend, payment_repo_depend, token_settings_repo_depend, discount_code_repo_depend
from src.routes.depends.service_depend import payment_service_depend
from src.routes.depends.bot_platform_depend import bot_platform_depend
from src.routes.depends.inline_keyboard_depend import inline_keyboard_depend

from src.gateway.external.interface.Ipayment_service import IPaymentService

from src.usecases.bot.add_credit.steps.show_current_credit import ShowCurrentCredit
from src.usecases.bot.add_credit.steps.request_summary import RequestSummary
from src.usecases.bot.add_credit.steps.payment import Payment

@inject
async def request_steps(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    callback_data: CallbackDataRequest | None = None,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    payment_repo: IPaymentRepo = Depends(payment_repo_depend),
    token_settings_repo: ITokenSettingsRepo = Depends(token_settings_repo_depend),
    discount_code_repo: IDiscountCodeRepo = Depends(discount_code_repo_depend),
    payment_service: IPaymentService = Depends(payment_service_depend),
    bot_platform: str = Depends(bot_platform_depend),
    inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
):
    
    start_point = callback_data is None
    
    chat_id = update.effective_user.id
    
    callback_data = callback_data or CallbackDataRequest(name=request_name, message_id=update.message.message_id)
    
    if start_point:
                
        request = ShowCurrentCredit(
            cache_repo,
            user_repo,
            bot_platform,
            inline_keyboard,
        )
        
        text, keyboard = await request.execute(callback_data, chat_id)
                
        await update.effective_message.reply_text(
            text=text,
            reply_markup=keyboard,
        )
             
    elif callback_data.step == ShowCurrentCredit.step:
                
        request = ShowCurrentCredit(
            cache_repo,
            user_repo,
            bot_platform,
            inline_keyboard,
        )
        
        text, keyboard = await request.execute(callback_data, chat_id)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )
        
    elif callback_data.step == RequestSummary.step:
                
        request = RequestSummary(
            cache_repo,
            user_repo,
            token_settings_repo,
            discount_code_repo,
            inline_keyboard,
        )
        
        text, keyboard = await request.execute(callback_data, chat_id)
        
        await update.effective_message.reply_text(
            text=text,
            reply_markup=keyboard,
        )
            
    elif callback_data.step == Payment.step:
                
        request = Payment(
            cache_repo,
            user_repo,
            token_settings_repo,
            payment_repo,
            payment_service,
            bot_platform,
            inline_keyboard,
        )
        
        text, keyboard = await request.execute(callback_data, chat_id)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )