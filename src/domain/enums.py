from enum import Enum

class ExpirationType(str, Enum):
    minutes = "minutes"
    hours = "hours"
    day = "day"
    
class PlatformEntities(str, Enum):
    telegram = "telegram"
    bale = "bale"
    rubika = "rubika"
    
class PaymentStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    paid = "paid"
    canceled = "canceled"
    rejected = "rejected"