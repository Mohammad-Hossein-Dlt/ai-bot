from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.discount_code.update_discount_code_input import UpdateDiscountCodeInput
from src.usecases.discount_code.update_discount_code import UpdateDiscountCode
from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.routes.depends.repo_depend import discount_code_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def update_discount_code(
    discount_code: UpdateDiscountCodeInput = Query(...),
    discount_code_repo: IDiscountCodeRepo = Depends(discount_code_repo_depend),
):
    try:
        update_discount_code_usecase = UpdateDiscountCode(discount_code_repo)
        output = await update_discount_code_usecase.execute(discount_code)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
