from pydantic import BaseModel, ConfigDict

class JWTParams(BaseModel):
    secret: str
    algorithm: str
    access_expiration_minutes: int
    refresh_expiration_minutes: int
    
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
