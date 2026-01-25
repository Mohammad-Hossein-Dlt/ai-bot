from pydantic import BaseModel

class CreateBotSettingsInput(BaseModel):
    enable_bot: bool