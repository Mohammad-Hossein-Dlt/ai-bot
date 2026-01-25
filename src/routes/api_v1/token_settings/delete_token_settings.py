from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.token_settings.delete_token_settings import DeleteTokenSettings
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.routes.depends.repo_depend import token_settings_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def delete_token_settings(
    token_settings_repo: ITokenSettingsRepo = Depends(token_settings_repo_depend),
):
    try:
        delete_token_settings_usecase = DeleteTokenSettings(token_settings_repo)
        output = await delete_token_settings_usecase.execute()
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
