from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.repo.interface.Iuser_repo import IUserRepo
from src.gateway.external.interface.Ipayment_service import IPaymentService
from src.models.schemas.payment.payment_input import PaymentInput
from src.models.schemas.payment.payment_output import PaymentOutput
from src.domain.schemas.payment.payment_model import PaymentModel
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreatePayment:
    
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
        payment: PaymentInput,
    ) -> PaymentOutput:
        
        try:
            user: UserModel = await self.user_repo.get_by_chat_id(payment.chat_id)
            # payment_record = self.payment_repo.get_by_id()
            to_create: PaymentModel = PaymentModel.model_validate(payment, from_attributes=True)
            to_create.user_id = user.id
            
            created_payment: PaymentModel = await self.payment_repo.create(to_create)
            to_create.id = created_payment.id
            
            try:
                payment_link, authority = await self.payment_service.payment_request(to_create)
            except:
                await self.payment_repo.delete_by_id(to_create.id)
                raise
            
            to_create.authority = authority
            await self.payment_repo.modify(to_create)
            
            return PaymentOutput(payment_id=str(to_create.id), payment_link=payment_link)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 