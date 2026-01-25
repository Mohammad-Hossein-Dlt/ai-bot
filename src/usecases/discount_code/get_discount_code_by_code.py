from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.domain.schemas.discount_code.discount_code_model import DiscountCodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetDiscountCodeByCode:
    
    def __init__(
        self,
        discount_code_repo: IDiscountCodeRepo,
    ):
        
        self.discount_code_repo = discount_code_repo
    
    async def execute(
        self,
        code: str,
    ) -> DiscountCodeModel:
        
        try:
            return await self.discount_code_repo.get_by_code(code)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 