from fast_depends import inject, Depends
from src.domain.schemas.user.user_model import UserModel
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from .general_buttons import home_markup
from raw_texts.raw_texts import CLOSE_PANEL
from src.infra.utils.number_converter import english_to_persian, number_formatter
import json


@inject
async def show_profile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    user_repo: IUserRepo = Depends(user_repo_depend),
):

    user_id = update.effective_user.id
    user: UserModel = await user_repo.get_by_chat_id(user_id)

    if not user:
        user_not_found = 'کاربر وجود ندارد!'
        await update.message.reply_text(
            text=user_not_found,
            reply_markup=home_markup,
        )
        return

    wallet_credit = f"شناسه کاربری شما: user_id"
    wallet_credit = wallet_credit.replace("user_id", str(user_id))

    profile_buttons = [
        [
            InlineKeyboardButton("💎 توکن‌های‌شما", callback_data="None1"),
            InlineKeyboardButton(f"{english_to_persian(number_formatter(int(user.tokens)))} عدد", callback_data="None2"),
        ],
        [
            InlineKeyboardButton(
                CLOSE_PANEL,
                callback_data=f"close:{update.message.message_id}"
            ),
        ],
    ]
    
    profile_markup = InlineKeyboardMarkup(inline_keyboard=profile_buttons)
    
    await update.message.reply_text(
        text=wallet_credit,
        reply_to_message_id=update.message.message_id,
        reply_markup=profile_markup,
    )
