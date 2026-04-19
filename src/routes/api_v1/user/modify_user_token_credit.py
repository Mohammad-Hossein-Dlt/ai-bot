from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.domain.enums import PlatformEntities
from src.models.schemas.user.modify_user_token_credit_input import ModifyUserTokenCreditInput
from src.usecases.user.modify_token_credit import ModifyUserTokenCredit
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/modify-token-credit",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def modify_token_credit(
    modify_user_token: ModifyUserTokenCreditInput = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        modify_usecase = ModifyUserTokenCredit(user_repo, modify_user_token.bot_platform)
        output = await modify_usecase.execute(modify_user_token)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
