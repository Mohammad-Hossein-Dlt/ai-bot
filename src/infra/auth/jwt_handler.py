import jwt
from src.infra.schemas.auth.jwt_params import JWTParams
from src.domain.schemas.auth.jwt_payload import JWTPayload
from src.infra.exceptions.exceptions import InvalidTokenException
from datetime import datetime, timezone, timedelta

class JWTHandler:

    def __init__(
        self,
        context: JWTParams,
    ):
        self.context = context
    
    def create_jwt_token(
        self,
        payload: JWTPayload,
    ) -> str:
        
        now = datetime.now(timezone.utc).replace(microsecond=0)
        
        if payload.type == "access":
            payload.exp = now + timedelta(minutes=self.context.access_expiration_minutes)
        elif payload.type == "refresh":
            payload.exp = now + timedelta(minutes=self.context.refresh_expiration_minutes)
        
        return jwt.encode(payload.model_dump(), self.context.secret, self.context.algorithm)

    def decode_jwt_token(
        self,
        token: str,
    ) -> JWTPayload:
        try:
            payload = jwt.decode(token, self.context.secret, algorithms=[self.context.algorithm])
        except jwt.exceptions.PyJWTError as ex:            
            raise InvalidTokenException(status_code=401, message=str(ex))
        
        return JWTPayload.model_validate(payload)