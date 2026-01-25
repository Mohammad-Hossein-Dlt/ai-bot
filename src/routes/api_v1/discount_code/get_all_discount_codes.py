from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.discount_code.get_all_discount_codes import GetAllDiscountCodes
from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.routes.depends.repo_depend import discount_code_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/all",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def get_all_discount_codes(
    discount_code_repo: IDiscountCodeRepo = Depends(discount_code_repo_depend),
):
    try:
        get_all_discount_codes_usecase = GetAllDiscountCodes(discount_code_repo)
        outputs_list = await get_all_discount_codes_usecase.execute()
        return [ output.model_dump(mode="json") for output in outputs_list ]
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
