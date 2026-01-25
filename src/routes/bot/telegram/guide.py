from telegram import Update
from telegram.ext import ContextTypes
from raw_texts.raw_texts import GUIDE_TEXT


async def guide(update: Update, context: ContextTypes.DEFAULT_TYPE,):
    await update.message.reply_text(GUIDE_TEXT)
