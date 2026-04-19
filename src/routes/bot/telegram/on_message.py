from telegram import Update
from telegram.ext import ContextTypes

from .content_creation.ai_answer import request_steps as content_creation_request_steps
from .text_to_image.ai_answer import request_steps as text_to_image_request_steps
from .text_to_audio.ai_answer import request_steps as text_to_audio_request_steps
from .audio_to_text.ai_answer import request_steps as audio_to_text_request_steps
from .add_credit.add_credit import request_steps as add_credit_request_steps
from .profile.profile import request_steps as profile_request_steps
from .pricing.pricing import request_steps as pricing_request_steps
from .guide.guide import request_steps as guide_request_steps

from .buttons import home_markup

from raw_texts.raw_texts import *

async def on_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    
    text = update.effective_message.text
    
    if text == CONTENT_CREATION:
        await content_creation_request_steps(update, context)
    elif text == TEXT_TO_IMAGE:
        await text_to_image_request_steps(update, context)
    elif text == TEXT_TO_AUDIO:
        await text_to_audio_request_steps(update, context)
    elif text == AUDIO_TO_TEXT:
        await audio_to_text_request_steps(update, context)
    elif text == PROFILE:
        await profile_request_steps(update, context)
    elif text == ADD_CREDIT:
        await add_credit_request_steps(update, context)
    elif text == PRICING:
        await pricing_request_steps(update, context)
    elif text == GUIDE:
        await guide_request_steps(update, context)
    elif text == BACK:
        await update.message.reply_text(
            text=RESTART,
            reply_markup=home_markup,
        )