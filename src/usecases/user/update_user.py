from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.user.update_user_input import UpdateUserInput
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        bot_platform: str,
    ):
        
        self.user_repo = user_repo
        self.bot_platform = bot_platform
    
    async def execute(
        self,
        user: UpdateUserInput,
    ) -> UserModel:
        
        try:
            
            to_update = UserModel()
            
            if user.user_id:
                to_update = await self.user_repo.get_by_id(user.user_id)
            if user.chat_id:
                to_update = await self.user_repo.get_by_chat_id(user.chat_id, self.bot_platform)
                
            return await self.user_repo.update(to_update)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 