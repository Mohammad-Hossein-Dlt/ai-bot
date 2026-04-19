from ._router import router
from fastapi import Request, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.routes.depends.repo_depend import payment_repo_depend, user_repo_depend
from src.routes.depends.service_depend import payment_service_depend
from src.usecases.payment.verify_payment import VerifyPayment
from src.infra.fastapi_config.template_engine import templates
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/verify",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def verify_payment(
    request: Request,
    payment_id: str,
    Authority: str,
    Status: str,
    payment_repo: IPaymentRepo = Depends(payment_repo_depend),
    user_repo: IUserRepo = Depends(user_repo_depend),
    payment_service: IPaymentService = Depends(payment_service_depend),
):
    try:
        create_payment_usecase = VerifyPayment(payment_repo, user_repo, payment_service)
        output = await create_payment_usecase.execute(payment_id, Authority, Status)
        return templates.TemplateResponse(request, "success_payment.html", {"payment": output.model_dump(mode="json")})
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
