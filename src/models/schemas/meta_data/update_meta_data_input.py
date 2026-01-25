from pydantic import BaseModel

class UpdateMetaDataInput(BaseModel):
    channel_id: str | None = None
    support_id: str | None = None
    bot_id: str | None = None