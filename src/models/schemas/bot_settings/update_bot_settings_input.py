from pydantic import BaseModel

class UpdateBotSettingsInput(BaseModel):
    enable_bot: bool | None = None