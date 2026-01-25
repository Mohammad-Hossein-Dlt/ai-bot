from src.infra.settings.settings import settings
from src.infra.schemas.auth.jwt_params import JWTParams

def init_jwt() -> JWTParams:
    return JWTParams.model_validate(settings.JWT)