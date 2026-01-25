from pydantic import BaseModel

class CreateMetaDataInput(BaseModel):
    channel_id: str
    support_id: str
    bot_id: str