from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.enums import PlatformEntities
from src.usecases.user.delete_user_by_chat_id import DeleteUserByChatId
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/chat-id",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def delete_user_by_chat_id(
    chat_id: str = Query(...),
    bot_platform: PlatformEntities = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        delete_user_by_chat_id_usecase = DeleteUserByChatId(user_repo, bot_platform)
        output = await delete_user_by_chat_id_usecase.execute(chat_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
