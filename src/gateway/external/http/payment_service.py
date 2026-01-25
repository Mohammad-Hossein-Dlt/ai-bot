import aiohttp
from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.domain.schemas.payment.payment_model import PaymentModel
from src.infra.exceptions.exceptions import AppBaseException
import uuid

class PaymentService(IPaymentService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str,
    ):  
        self.session = session
        self.base_url = base_url
        self.allowed_status_codes = [200, 201]
    
    async def payment_request(
        self,
        payment: PaymentModel,
    ) -> tuple[str, str]:
                    
        payload = {
            'merchant_id': str(uuid.uuid4()),
            "authority": payment.authority,
            'amount': payment.amount,
            'description': 'description',
            'callback_url': "https://localhost/verify",
        }
                
        response = await self.session.post(
            "https://sandbox.zarinpal.com/pg/v4/payment/request.json",
            json=payload,
        )
        
        if response.status in self.allowed_status_codes:
            data = await response.json()
            authority = data["data"]["authority"]
            return f"https://sandbox.zarinpal.com/pg/StartPay/{authority}", authority
        else:
            data = await response.json()
            detail = data["errors"]["message"]
            raise AppBaseException(response.status, detail)