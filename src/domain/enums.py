from enum import Enum

class ExpirationType(str, Enum):
    minutes = "minutes"
    hours = "hours"
    day = "day"
    
class PlatformEntities(str, Enum):
    telegram = "telegram"
    bale = "bale"
    rubika = "rubika"
    
class AiPlatformType(str, Enum):
    google = "google"
    open_ai = "open-ai"        

class AiActionType(str, Enum):
    content_creation = "content_creation"
    text_to_image = "text_to_image"
    audio_to_text = "audio_to_text"
    text_to_audio = "text_to_audio"

class PaymentStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    paid = "paid"
    canceled = "canceled"
    rejected = "rejected"