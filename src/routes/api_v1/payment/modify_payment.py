from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.payment.modify_payment_input import ModifyPaymentInput
from src.usecases.payment.modify_payment import ModifyPayment
from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.routes.depends.repo_depend import payment_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def modify_payment(
    payment: ModifyPaymentInput = Query(...),
    payment_repo: IPaymentRepo = Depends(payment_repo_depend),
):
    try:
        modify_payment_usecase = ModifyPayment(payment_repo)
        output = await modify_payment_usecase.execute(payment)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
