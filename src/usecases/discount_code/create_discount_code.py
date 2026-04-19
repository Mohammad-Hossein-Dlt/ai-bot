from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.models.schemas.discount_code.create_discount_code_input import CreateDiscountCodeInput
from src.domain.schemas.discount_code.discount_code_model import DiscountCodeModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException
from datetime import datetime, timedelta, timezone

class CreateDiscountCode:
    
    def __init__(
        self,
        discount_code_repo: IDiscountCodeRepo,
    ):
        
        self.discount_code_repo = discount_code_repo
    
    async def execute(
        self,
        new_discount_code: CreateDiscountCodeInput,
    ) -> DiscountCodeModel:
        
        try:
            to_create: DiscountCodeModel = DiscountCodeModel.model_validate(new_discount_code, from_attributes=True)
            
            expires_at = timedelta()
            if new_discount_code.expiration_type == "minutes":
                expires_at = timedelta(minutes=new_discount_code.expires_at)
            if new_discount_code.expiration_type == "hours":
                expires_at = timedelta(hours=new_discount_code.expires_at)
            if new_discount_code.expiration_type == "day":
                expires_at = timedelta(days=new_discount_code.expires_at)
                
            to_create.expires_at = datetime.now(timezone.utc) + expires_at
                
            return await self.discount_code_repo.create(to_create)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 