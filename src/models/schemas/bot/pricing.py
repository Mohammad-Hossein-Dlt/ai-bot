from pydantic import BaseModel

class PricingRequestModel(BaseModel):
    ai_action_type_fa: str | None = None