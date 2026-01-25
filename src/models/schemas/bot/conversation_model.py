from pydantic import BaseModel
from .callback_request import CallbackDataRequest

class ConversationModel(BaseModel):
    callback_data: CallbackDataRequest
    messages: dict = {}

