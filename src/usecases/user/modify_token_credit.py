from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.user.modify_user_token_credit_input import ModifyUserTokenCreditInput
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ModifyUserTokenCredit:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo
    
    async def execute(
        self,
        modify: ModifyUserTokenCreditInput,
    ) -> UserModel:
        
        try:
            return await self.user_repo.modify_token_credit(modify.chat_id, modify.value)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 