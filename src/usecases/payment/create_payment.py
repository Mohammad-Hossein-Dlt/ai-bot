from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.models.schemas.payment.create_payment_input import CreatePaymentInput
from src.models.schemas.payment.payment_output import PaymentOutput
from src.domain.schemas.payment.payment_model import PaymentModel
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreatePayment:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        payment_repo: IPaymentRepo,
        payment_service: IPaymentService,
        bot_platform: str,
    ):
        
        self.user_repo = user_repo
        self.payment_repo = payment_repo
        self.payment_service = payment_service
        self.bot_platform = bot_platform

    
    async def execute(
        self,
        new_payment: CreatePaymentInput,
    ) -> PaymentOutput:
        
        try:
            user: UserModel = await self.user_repo.get_by_chat_id(new_payment.chat_id, self.bot_platform)
            to_create: PaymentModel = PaymentModel.model_validate(new_payment, from_attributes=True)
            to_create.user_id = user.id
            
            payment: PaymentModel = await self.payment_repo.create(to_create)
            
            try:
                payment_link, authority = await self.payment_service.payment_request(payment)
            except:
                await self.payment_repo.delete_by_id(payment.id)
                raise
            
            payment.authority = authority
            await self.payment_repo.modify(payment)
            
            return PaymentOutput(payment_id=str(payment.id), payment_link=payment_link)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 