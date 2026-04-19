from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetUserByChatId:
    
    def __init__(
        self,
        user_repo: IUserRepo,
        bot_platform: str,
    ):
        
        self.user_repo = user_repo
        self.bot_platform = bot_platform
    
    async def execute(
        self,
        chat_id: str,
    ) -> UserModel:
        
        try:
            return await self.user_repo.get_by_chat_id(chat_id, self.bot_platform)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 