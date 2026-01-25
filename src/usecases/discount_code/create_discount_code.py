from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.models.schemas.discount_code.create_discount_code_input import CreateDiscountCodeInput
from src.domain.schemas.discount_code.discount_code_model import DiscountCodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateDiscountCode:
    
    def __init__(
        self,
        discount_code_repo: IDiscountCodeRepo,
    ):
        
        self.discount_code_repo = discount_code_repo
    
    async def execute(
        self,
        discount_code: CreateDiscountCodeInput,
    ) -> DiscountCodeModel:
        
        try:
            to_create: DiscountCodeModel = DiscountCodeModel.model_validate(discount_code, from_attributes=True)
            return await self.discount_code_repo.create(to_create)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 