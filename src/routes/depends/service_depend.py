from src.infra.context.app_context import AppContext

from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.gateway.external.http.payment_service import PaymentService

def payment_service_depend() -> IPaymentService:
    
    return PaymentService(
        AppContext.http_client,
        "",
    )