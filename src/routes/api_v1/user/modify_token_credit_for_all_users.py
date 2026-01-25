from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.user.modify_token_credit_for_all_users import ModifyTokenCreditForAllUsers
from src.repo.interface.Iuser_repo import IUserRepo
from src.routes.depends.repo_depend import user_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/modify-token-credit/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def modify_token_credit_for_all_users(
    value: int,
    user_repo: IUserRepo = Depends(user_repo_depend),
):
    try:
        modify_usecase = ModifyTokenCreditForAllUsers(user_repo)
        output = await modify_usecase.execute(value)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
