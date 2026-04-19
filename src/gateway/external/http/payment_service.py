import aiohttp
from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.domain.schemas.payment.payment_model import PaymentModel
from src.models.schemas.payment.verify_payment_input import VerifyPaymentInput
from src.models.schemas.payment.verify_payment_output import VerifyPaymentOutput
from src.infra.exceptions.exceptions import AppBaseException

class PaymentService(IPaymentService):
    
    def __init__(
        self,
        session: aiohttp.ClientSession,
        base_url: str,
        merchant_id: str,
    ):
        
        self.session = session
        self.base_url = base_url
        self.merchant_id = merchant_id
        
        self.allowed_status_codes = [200, 201]
    
    async def payment_request(
        self,
        payment: PaymentModel,
    ) -> tuple[str, str]:
                    
        payload = {
            'merchant_id': self.merchant_id,
            "authority": payment.authority,
            'amount': payment.amount,
            'description': 'description',
            'callback_url': f"http://127.0.0.1:8000/api-service/api/v1/payment/verify?payment_id={payment.id}",
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
        
    async def verify_request(
        self,
        to_verify: VerifyPaymentInput,
    ) -> VerifyPaymentOutput:
                            
        payload = {
            'merchant_id': self.merchant_id,
            'amount': to_verify.amount,
            'authority': to_verify.authority,
        }
                
        response = await self.session.post(
            "https://sandbox.zarinpal.com/pg/v4/payment/verify.json",
            json=payload,
        )
        
        if response.status in self.allowed_status_codes:
            
            data = await response.json()
            code = data["data"]["code"]
            ref_id = data["data"]["ref_id"]
            
            return VerifyPaymentOutput(code=code, ref_id=str(ref_id))
        
        else:
            data = await response.json()
            detail = data["errors"]["message"]
            raise AppBaseException(response.status, detail)