from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.bot_settings.update_bot_settings_input import UpdateBotSettingsInput
from src.usecases.bot_settings.update_bot_settings import UpdateBotSettings
from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.routes.depends.repo_depend import bot_settings_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def update_bot_settings(
    bot_settings: UpdateBotSettingsInput = Query(...),
    bot_settings_repo: IBotSettingsRepo = Depends(bot_settings_repo_depend),
):
    try:
        update_bot_settings_usecase = UpdateBotSettings(bot_settings_repo)
        output = await update_bot_settings_usecase.execute(bot_settings)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
