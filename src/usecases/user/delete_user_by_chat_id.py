from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class DeleteUserByChatId:
    
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
    ) -> OperationOutput:
        
        try:
            status = await self.user_repo.delete_by_chat_id(chat_id, self.bot_platform)
            return OperationOutput(id=chat_id, request="delete/user", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 