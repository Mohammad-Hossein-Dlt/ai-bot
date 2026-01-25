from pydantic import BaseModel, model_validator, field_validator
from typing import Literal
from datetime import datetime

class JWTPayload(BaseModel):
    user_id: int | str
    type: Literal["access", "refresh"]
    exp: datetime | None = None
    
    @model_validator(mode="before")
    def validator_before(cls, values) -> dict:
                
        if isinstance(values, dict):
            for k, v in values.items():
                try:
                    v = int(v)
                except:
                    pass
                
                values[k] = v
        
        return values
    
    @field_validator("*")
    def object_id_validator(cls, var):
        try:
            return int(var)
        except:
            pass
        
        return var