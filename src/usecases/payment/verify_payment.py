from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.domain.schemas.payment.payment_model import PaymentModel
from src.models.schemas.payment.verify_payment_input import VerifyPaymentInput
from src.models.schemas.payment.verify_payment_output import VerifyPaymentOutput
from src.models.schemas.payment.success_payment_output import SuccessPaymentOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class VerifyPayment:
    
    def __init__(
        self,
        payment_repo: IPaymentRepo,
        user_repo: IUserRepo,
        payment_service: IPaymentService,
    ):
        
        self.payment_repo = payment_repo
        self.user_repo = user_repo
        self.payment_service = payment_service

    
    async def execute(
        self,
        payment_id: str,
        authority: str,
        status: str,
    ) -> SuccessPaymentOutput | None:
        
        try:
            
            if status == "NOK":
                return None
            
            payment: PaymentModel = await self.payment_repo.get_by_id(payment_id)
            
            verify: VerifyPaymentOutput = await self.payment_service.verify_request(
                VerifyPaymentInput(
                    amount=payment.amount,
                    authority=authority,
                ),
            )
                        
            if verify.code == 100:
                
                user = await self.user_repo.get_by_id(payment.user_id)
                await self.user_repo.modify_token_credit(user, payment.tokens)
                
            payment.ref_id = verify.ref_id
            await self.payment_repo.modify(payment)
            
            return SuccessPaymentOutput(tokens=payment.tokens, amount=payment.amount, code=verify.code, ref_id=verify.ref_id)
        
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 