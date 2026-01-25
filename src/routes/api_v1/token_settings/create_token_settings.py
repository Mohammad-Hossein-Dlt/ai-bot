from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.token_settings.create_token_settings_input import CreateTokenSettingsInput
from src.usecases.token_settings.create_token_settings import CreateTokenSettings
from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.routes.depends.repo_depend import token_settings_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def create_token_settings(
    token_settings: CreateTokenSettingsInput = Query(...),
    token_settings_repo: ITokenSettingsRepo = Depends(token_settings_repo_depend),
):
    try:
        create_token_settings_usecase = CreateTokenSettings(token_settings_repo)
        output = await create_token_settings_usecase.execute(token_settings)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
