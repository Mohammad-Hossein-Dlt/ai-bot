from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.operation.operation_output import OperationOutput
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class ModifyTokenCreditForAllUsers:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo
    
    async def execute(
        self,
        value: int,
    ) -> OperationOutput:
        
        try:
            status = await self.user_repo.modify_token_credit_for_all_users(value)
            return OperationOutput(id=None, request="modify_token/user/all", status=status)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 