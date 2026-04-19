from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.payment.create_payment_input import CreatePaymentInput
from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.routes.depends.repo_depend import payment_repo_depend, user_repo_depend
from src.routes.depends.service_depend import payment_service_depend
from src.routes.depends.bot_platform_depend import bot_platform_depend
from src.usecases.payment.create_payment import CreatePayment
from src.infra.exceptions.exceptions import AppBaseException

@router.post(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def create_payment(
    new_payment: CreatePaymentInput = Query(...),
    user_repo: IUserRepo = Depends(user_repo_depend),
    payment_repo: IPaymentRepo = Depends(payment_repo_depend),
    payment_service: IPaymentService = Depends(payment_service_depend),
    bot_platform: str = Depends(bot_platform_depend),
):
    try:
        create_payment_usecase = CreatePayment(user_repo, payment_repo, payment_service, bot_platform)
        output = await create_payment_usecase.execute(new_payment)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
