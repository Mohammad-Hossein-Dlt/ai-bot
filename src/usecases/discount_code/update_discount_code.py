from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.models.schemas.discount_code.update_discount_code_input import UpdateDiscountCodeInput
from src.domain.schemas.discount_code.discount_code_model import DiscountCodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateDiscountCode:
    
    def __init__(
        self,
        discount_code_repo: IDiscountCodeRepo,
    ):
        
        self.discount_code_repo = discount_code_repo
    
    async def execute(
        self,
        discount_code: UpdateDiscountCodeInput,
    ) -> DiscountCodeModel:
        
        try:
            to_update: DiscountCodeModel = DiscountCodeModel.model_validate(discount_code, from_attributes=True)
            return await self.discount_code_repo.update(to_update)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 