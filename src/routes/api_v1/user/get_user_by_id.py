from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.user.get_user_by_id import GetUserById
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/id",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def get_user_by_id(
    user_id: str,
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        get_user_by_id_usecase = GetUserById(user_repo)
        output = await get_user_by_id_usecase.execute(user_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
