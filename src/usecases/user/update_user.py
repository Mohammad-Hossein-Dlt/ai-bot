from src.repo.interface.Iuser_repo import IUserRepo
from src.models.schemas.user.create_user_input import CreateUserInput
from src.domain.schemas.user.user_model import UserModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateUser:
    
    def __init__(
        self,
        user_repo: IUserRepo,
    ):
        
        self.user_repo = user_repo
    
    async def execute(
        self,
        user: CreateUserInput,
    ) -> UserModel:
        
        try:
            to_update: UserModel = UserModel.model_validate(user, from_attributes=True)
            return await self.user_repo.update(to_update)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 