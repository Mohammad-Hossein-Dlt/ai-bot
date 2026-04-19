from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.user.modify_user_token_credit_input import ModifyUserTokenCreditInput
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ModifyUserTokenCredit:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        bot_platform: str,
    ):
        
        self.user_repo = user_repo
        self.bot_platform = bot_platform
    
    async def execute(
        self,
        modify_user_token: ModifyUserTokenCreditInput,
    ) -> UserModel:
        
        try:
            user: UserModel = None
            
            if modify_user_token.user_id:
                user = await self.user_repo.get_by_id(modify_user_token.user_id)
            if modify_user_token.chat_id:
                user = await self.user_repo.get_by_chat_id(modify_user_token.chat_id, self.bot_platform)
                
            return await self.user_repo.modify_token_credit(user, modify_user_token.value)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 