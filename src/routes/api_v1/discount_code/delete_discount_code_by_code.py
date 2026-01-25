from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.discount_code.delete_discount_code_by_code import DeleteDiscountCodeByCode
from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.routes.depends.repo_depend import discount_code_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/code",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def delete_discount_code_by_code(
    code: str,
    discount_code_repo: IDiscountCodeRepo = Depends(discount_code_repo_depend),
):
    try:
        delete_discount_code_by_code_usecase = DeleteDiscountCodeByCode(discount_code_repo)
        output = await delete_discount_code_by_code_usecase.execute(code)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
