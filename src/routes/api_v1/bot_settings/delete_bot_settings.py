from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.bot_settings.delete_bot_settings import DeleteBotSettings
from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.routes.depends.repo_depend import bot_settings_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def delete_bot_settings(
    bot_settings_repo: IBotSettingsRepo = Depends(bot_settings_repo_depend),
):
    try:
        delete_bot_settings_usecase = DeleteBotSettings(bot_settings_repo)
        output = await delete_bot_settings_usecase.execute()
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
