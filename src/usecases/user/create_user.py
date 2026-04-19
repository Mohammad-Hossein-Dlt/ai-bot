from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.user.create_user_input import CreateUserInput
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.account_model import AccountModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo
    
    async def execute(
        self,
        new_user: CreateUserInput,
    ) -> UserModel:
        
        try:
            to_create: UserModel = UserModel(
                platform_accounts=[
                    AccountModel(
                        chat_id=new_user.chat_id,
                        platform=new_user.platform,
                    ),
                ],
            )
            return await self.user_repo.create(to_create)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")