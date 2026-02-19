from telegram import Update
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
from src.usecases.bot.add_credit.steps.show_current_credit import ShowCurrentCredit
from src.usecases.bot.add_credit.steps.payment import Payment

from raw_texts.raw_texts import CLOSE_PANEL

@inject
async def request_steps(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    callback_data: CallbackDataRequest | None = None,
    cache_repo: ICacheRepo = Depends(cache_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    token_settings_repo: ITokenSettingsRepo = Depends(token_settings_repo_depend),
    inline_keyboard: IInlineKeyboard = Depends(inline_keyboard_depend),
):
    
    start_point = callback_data is None
    
    chat_id = update.effective_user.id
    
    callback_data = callback_data or CallbackDataRequest(name=request_name, message_id=update.message.message_id)
    
    if start_point:
                
        request_summary = ShowCurrentCredit(user_repo, cache_repo, inline_keyboard)
        text, keyboard = await request_summary.execute(chat_id, callback_data)
                
        await update.effective_message.reply_text(
            text=text,
            reply_markup=keyboard,
        )
             
    elif callback_data.step == ShowCurrentCredit.step:
                
        request_summary = ShowCurrentCredit(user_repo, cache_repo, inline_keyboard)
        text, keyboard = await request_summary.execute(chat_id, callback_data)
                
        await update.effective_message.edit_text(
            text=text,
            reply_markup=keyboard,
        )
            
    elif callback_data.step == Payment.step:
                
        request_summary = Payment(user_repo, cache_repo, token_settings_repo, inline_keyboard)
        text, keyboard = await request_summary.execute(chat_id, callback_data)
                
        await update.effective_message.reply_text(
            text=text,
            reply_markup=keyboard,
        )
        
    # elif step == 1:
    #     await message.bot.delete_message(message.chat_id, message.message_id)
    #     await message.bot.send_message(
    #         chat_id=message.chat_id,
    #         text="🎁 لطفا کد تخفیف خود را ارسال کنید.",
    #     )
    #     answer_obj: Message = await client.wait_for('message', check=answer_checker2)

    #     db: Session = sessionLocal()

    #     discount_code = db.query(
    #         DiscountCode
    #     ).where(
    #         DiscountCode.Code == answer_obj.content,
    #         DiscountCode.ExpirationDate > datetime.now(pytz.UTC),
    #     ).first()

    #     token_settings = db.query(
    #         TokenSettings
    #     ).first()

    #     db.close()

    #     if not discount_code:
    #         await message.bot.send_message(
    #             text="❌ کد تخفیف یافت نشد.",
    #             chat_id=message.chat_id,
    #         )
    #         return

    #     deducted = (model.amount * discount_code.Percent) / 100
    #     amount = model.amount * (1 - (discount_code.Percent / 100))

    #     payment_url = f'{DOMAIN_URL}/api/v1/payment/request/?user_id={model.user_id}&payment_id={model.payment_id}&amount={amount}&tokens={model.tokens}'

    #     payment_text = "🥳 کد تخفیف با موفقیت اعمال شد و مبلغ deducted ريال از قیمت سرویس مورد نظر کسر شد"
    #     payment_text = payment_text.replace('deducted', english_to_persian(number_formatter(int(deducted))))

    #     payment_markup = InlineKeyboardMarkup()

    #     payment_markup.add(
    #         InlineKeyboardButton("💵 قیمت هر توکن:", callback_data="None1"),
    #         row=0,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton(f"{english_to_persian(number_formatter(token_settings.Unit))} ريال", callback_data="None2"),
    #         row=0,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton("💎 توکن درخواستی:", callback_data="None3"),
    #         row=2,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton(f"{english_to_persian(number_formatter(model.tokens))} عدد", callback_data="None4"),
    #         row=2,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton("💰 قیمت:", callback_data="None5"),
    #         row=4,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton(f"{english_to_persian(number_formatter(model.amount))} ریال", callback_data="None6"),
    #         row=4,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton("🎁 تخفیف:", callback_data="None7"),
    #         row=6,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton(f"{english_to_persian(number_formatter(int(deducted)))} ريال", callback_data="None8"),
    #         row=6,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton("💝 قیمت با تخفیف:", callback_data="None9"),
    #         row=8,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton(f"{english_to_persian(number_formatter(int(amount)))} ريال", callback_data="None10"),
    #         row=8,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton('✅ پرداخت', url=payment_url),
    #         row=10,
    #     )
    #     payment_markup.add(
    #         InlineKeyboardButton(
    #             CLOSE_PANEL,
    #             callback_data=json.dumps('close')
    #         ),
    #         row=12,
    #     )
    #     await message.bot.send_message(
    #         chat_id=message.chat_id,
    #         text=payment_text,
    #         components=payment_markup,
    #     )
