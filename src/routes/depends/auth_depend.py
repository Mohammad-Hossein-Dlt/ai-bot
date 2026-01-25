from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.infra.context.app_context import AppContext
from src.infra.auth.jwt_handler import JWTHandler
from .repo_depend import user_repo_depend
from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.usecases.user.user_get_self import UserGetSelf
from src.domain.enums import Role
from src.infra.exceptions.exceptions import AppBaseException
from typing import Literal

auth_schema = OAuth2PasswordBearer(tokenUrl="/auth/api/v1/login")

def jwt_handler_depend() -> JWTHandler:

    jwt_handler = JWTHandler(context=AppContext.jwt)
    return jwt_handler

async def auth_depend(
    token: str = Depends(auth_schema),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    token_type: Literal["access", "refresh"] = "access",
) -> UserModel:
    
    try:
        payload = jwt_handler.decode_jwt_token(token)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)
        
    if payload.type == token_type:
        get_user_usecase = UserGetSelf(user_repo)
        try:
            return await get_user_usecase.execute(payload.user_id)
        except AppBaseException as ex:
            raise HTTPException(status_code=ex.status_code, detail=ex.message)
    else:
        raise HTTPException(status_code=401, detail=f"You have not access with {payload.type}-token")
    
async def access_token_depend(
    token: str = Depends(auth_schema),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> UserModel:
    
    return await auth_depend(
        token,
        jwt_handler,
        user_repo,
        "access",
    )

async def refresh_token_depend(
    token: str = Depends(auth_schema),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> UserModel:
    
    return await auth_depend(
        token,
        jwt_handler,
        user_repo,
        "refresh",
    )
    
async def admin_auth_depend(
    token: str = Depends(auth_schema),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> UserModel:
    
    user: UserModel = await access_token_depend(
        token,
        jwt_handler,
        user_repo,
    )
    
    if user.role == Role.admin:
        return user
    else:
        raise HTTPException(status_code=401, detail="Only admin have access")    
    
async def user_auth_depend(
    token: str = Depends(auth_schema),
    jwt_handler: JWTHandler = Depends(jwt_handler_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
) -> UserModel:
    
    user: UserModel = await access_token_depend(
        token,
        jwt_handler,
        user_repo,
    )
    
    return user