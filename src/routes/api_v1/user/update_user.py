from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.enums import PlatformEntities
from src.models.schemas.user.update_user_input import UpdateUserInput
from src.usecases.user.update_user import UpdateUser
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def update_user(
    user: UpdateUserInput = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        update_user_usecase = UpdateUser(user_repo, user.bot_platform)
        output = await update_user_usecase.execute(user)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))

