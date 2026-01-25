from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.bot_settings.create_bot_settings_input import CreateBotSettingsInput
from src.usecases.bot_settings.create_bot_settings import CreateBotSettings
from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.routes.depends.repo_depend import bot_settings_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def create_bot_settings(
    bot_settings: CreateBotSettingsInput = Query(...),
    bot_settings_repo: IBotSettingsRepo = Depends(bot_settings_repo_depend),
):
    try:
        create_bot_settings_usecase = CreateBotSettings(bot_settings_repo)
        output = await create_bot_settings_usecase.execute(bot_settings)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
