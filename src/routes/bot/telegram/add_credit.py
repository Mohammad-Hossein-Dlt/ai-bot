# import uuid
# from datetime import datetime
# import pytz
# from bale import Bot, Message, InlineKeyboardButton, InlineKeyboardMarkup
# from bot_routers.general_buttons import home_markup, back_markup
# from config.config import DOMAIN_URL
# from data.models.payment_model import PaymentModel
# from raw_texts.raw_texts import BUTTONS, CLOSE_PANEL
# from utils.number_converter import persian_to_english, english_to_persian, number_formatter
# from database.connection import sessionLocal
# from database.models import TokenSettings, DiscountCode
# from sqlalchemy.orm import Session
# import json


# async def add_credit(message: Message, client: Bot, model: PaymentModel):
#     def answer_checker(m: Message):
#         return message.author == m.author and bool(message.text)

#     def answer_checker2(m: Message):
#         return model.user_id == m.author.user_id and bool(message.text)

#     step = model.step

#     if step == 0:

#         db: Session = sessionLocal()

#         token_settings = db.query(
#             TokenSettings
#         ).first()

#         db.close()

#         max_amount = token_settings.Max
#         min_amount = token_settings.Min

#         max_amount_formatted = english_to_persian(number_formatter(max_amount))
#         min_amount_formatted = english_to_persian(number_formatter(min_amount))

#         enter_tokens = 'تعداد توکنی که میخواهید کیف پولتان را شارژ کنید، وارد کنید.'
#         tokens_range = 'از تعداد min عدد تا تعداد max عدد، میتوانید توکن های کیف پولتان را شارژ کنید.'
#         tokens_range = tokens_range.replace('min', min_amount_formatted).replace('max', max_amount_formatted)
#         token_unit = 'قیمت هر واحد توکن unit ريال است'
#         token_unit = token_unit.replace("unit", english_to_persian(number_formatter(token_settings.Unit)))

#         await message.reply(
#             f'{enter_tokens}\n{tokens_range}\n{token_unit}',
#             components=back_markup,
#         )

#         answer_obj: Message = await client.wait_for('message', check=answer_checker)

#         if answer_obj.content in BUTTONS:
#             return

#         if not answer_obj.content.isnumeric():
#             await message.reply(
#                 'لطفا عدد وارد کنید.',
#                 components=home_markup,
#             )
#             return

#         tokens = int(persian_to_english(answer_obj.content))

#         if tokens > max_amount:
#             max_amount_error = f'تعداد وارد شده بیشتر از max عدد است.'
#             max_amount_error = max_amount_error.replace('max', max_amount_formatted)
#             await message.reply(
#                 max_amount_error,
#                 components=home_markup,
#             )
#             return

#         elif tokens < min_amount:
#             min_amount_error = f'مبلغ وارد شده کمتر از min عدد است.'
#             min_amount_error = min_amount_error.replace('min', min_amount_formatted)
#             await message.reply(
#                 min_amount_error,
#                 components=home_markup,
#             )
#             return

#         amount = tokens * token_settings.Unit

#         payment_id = str(uuid.uuid4())

#         payment_url = f'{DOMAIN_URL}/api/v1/payment/request/?user_id={message.author.user_id}&payment_id={payment_id}&amount={amount}&tokens={tokens}'

#         payment_text = 'لینک پرداخت برای خرید تعداد توکن مورد نظر ساخته شد. از طریق لینک زیر پرداخت کنید.'

#         payment_markup = InlineKeyboardMarkup()

#         payment_markup.add(
#             InlineKeyboardButton("💵 قیمت هر توکن:", callback_data="None1"),
#             row=0,
#         )
#         payment_markup.add(
#             InlineKeyboardButton( f"{english_to_persian(number_formatter(token_settings.Unit))} ريال", callback_data="None2"),
#             row=0,
#         )
#         payment_markup.add(
#             InlineKeyboardButton("💎 توکن درخواستی:", callback_data="None3"),
#             row=2,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(f"{english_to_persian(number_formatter(tokens))} عدد", callback_data="None4"),
#             row=2,
#         )
#         payment_markup.add(
#             InlineKeyboardButton("💰 قیمت:", callback_data="None5"),
#             row=4,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(f"{english_to_persian(number_formatter(amount))} ريال", callback_data="None6"),
#             row=4,
#         )

#         payment_markup.add(
#             InlineKeyboardButton(
#                 '🎁 اعمال کد تخفیف',
#                 callback_data=PaymentModel(
#                     section="payment",
#                     step=1,
#                     user_id=message.author.user_id,
#                     payment_id=payment_id,
#                     amount=amount,
#                     tokens=tokens,
#                 ).json()
#             ),
#             row=6,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(
#                 '✅ پرداخت',
#                 url=payment_url,
#             ),
#             row=8,
#         )

#         payment_markup.add(
#             InlineKeyboardButton(
#                 CLOSE_PANEL,
#                 callback_data=json.dumps('close')
#             ),
#             row=10,
#         )
#         await message.bot.send_message(
#             chat_id=message.chat_id,
#             text=payment_text,
#             components=payment_markup,
#         )

#     elif step == 1:
#         await message.bot.delete_message(message.chat_id, message.message_id)
#         await message.bot.send_message(
#             chat_id=message.chat_id,
#             text="🎁 لطفا کد تخفیف خود را ارسال کنید.",
#         )
#         answer_obj: Message = await client.wait_for('message', check=answer_checker2)

#         db: Session = sessionLocal()

#         discount_code = db.query(
#             DiscountCode
#         ).where(
#             DiscountCode.Code == answer_obj.content,
#             DiscountCode.ExpirationDate > datetime.now(pytz.UTC),
#         ).first()

#         token_settings = db.query(
#             TokenSettings
#         ).first()

#         db.close()

#         if not discount_code:
#             await message.bot.send_message(
#                 text="❌ کد تخفیف یافت نشد.",
#                 chat_id=message.chat_id,
#             )
#             return

#         deducted = (model.amount * discount_code.Percent) / 100
#         amount = model.amount * (1 - (discount_code.Percent / 100))

#         payment_url = f'{DOMAIN_URL}/api/v1/payment/request/?user_id={model.user_id}&payment_id={model.payment_id}&amount={amount}&tokens={model.tokens}'

#         payment_text = "🥳 کد تخفیف با موفقیت اعمال شد و مبلغ deducted ريال از قیمت سرویس مورد نظر کسر شد"
#         payment_text = payment_text.replace('deducted', english_to_persian(number_formatter(int(deducted))))

#         payment_markup = InlineKeyboardMarkup()

#         payment_markup.add(
#             InlineKeyboardButton("💵 قیمت هر توکن:", callback_data="None1"),
#             row=0,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(f"{english_to_persian(number_formatter(token_settings.Unit))} ريال", callback_data="None2"),
#             row=0,
#         )
#         payment_markup.add(
#             InlineKeyboardButton("💎 توکن درخواستی:", callback_data="None3"),
#             row=2,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(f"{english_to_persian(number_formatter(model.tokens))} عدد", callback_data="None4"),
#             row=2,
#         )
#         payment_markup.add(
#             InlineKeyboardButton("💰 قیمت:", callback_data="None5"),
#             row=4,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(f"{english_to_persian(number_formatter(model.amount))} ریال", callback_data="None6"),
#             row=4,
#         )
#         payment_markup.add(
#             InlineKeyboardButton("🎁 تخفیف:", callback_data="None7"),
#             row=6,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(f"{english_to_persian(number_formatter(int(deducted)))} ريال", callback_data="None8"),
#             row=6,
#         )
#         payment_markup.add(
#             InlineKeyboardButton("💝 قیمت با تخفیف:", callback_data="None9"),
#             row=8,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(f"{english_to_persian(number_formatter(int(amount)))} ريال", callback_data="None10"),
#             row=8,
#         )
#         payment_markup.add(
#             InlineKeyboardButton('✅ پرداخت', url=payment_url),
#             row=10,
#         )
#         payment_markup.add(
#             InlineKeyboardButton(
#                 CLOSE_PANEL,
#                 callback_data=json.dumps('close')
#             ),
#             row=12,
#         )
#         await message.bot.send_message(
#             chat_id=message.chat_id,
#             text=payment_text,
#             components=payment_markup,
#         )
