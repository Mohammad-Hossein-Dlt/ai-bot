from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.payment.delete_payment_by_user_id import DeletePaymentByUserId
from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.routes.depends.repo_depend import payment_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/user-id",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def delete_payment_by_user_id(
    user_id: str,
    payment_repo: IPaymentRepo = Depends(payment_repo_depend),
):
    try:
        delete_payment_by_user_id_usecase = DeletePaymentByUserId(payment_repo)
        output = await delete_payment_by_user_id_usecase.execute(user_id)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
