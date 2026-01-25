from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.user.create_user_input import CreateUserInput
from src.usecases.user.create_user import CreateUser
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def create_user(
    user: CreateUserInput = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        create_user_usecase = CreateUser(user_repo)
        output = await create_user_usecase.execute(user)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
