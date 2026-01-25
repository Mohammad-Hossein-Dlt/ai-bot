from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.database.mongodb.collections.user_collection import UserCollection
from bson.objectid import ObjectId
from src.infra.exceptions.exceptions import EntityNotFoundError, InvalidRequestException

class UserMongodbRepo(IUserRepo):
            
    async def create(
        self,
        user: UserModel,
    ) -> UserModel:

        try:
            await self.get_by_chat_id(user.chat_id)
            raise InvalidRequestException(409, "User already exist")
        except EntityNotFoundError:
            new_user = await UserCollection.insert(
                UserCollection(**user.model_dump(exclude={"id", "_id"})),
            )
            return UserModel.model_validate(new_user, from_attributes=True)
    
    async def get_by_id(
        self,
        user_id: str,
    ) -> UserModel:
    
        try:
            user = await UserCollection.get(user_id)
            return UserModel.model_validate(user, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
        
    async def get_by_chat_id(
        self,
        chat_id: str,
    ) -> UserModel:
    
        try:
            user = await UserCollection.find(
                UserCollection.chat_id == chat_id,
            ).first_or_none()
            return UserModel.model_validate(user, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def update(
        self,
        user: UserModel,
    ) -> bool:
        
        try:                
            to_update: dict = user.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                },
                db_stack="no-sql",
            )
                        
            await UserCollection.find_one(
                UserCollection.id == user.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_chat_id(user.chat_id)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def add_token_credit(
        self,
        chat_id: str,
        value: int,
    ) -> bool:
    
        try: 
            
            user = await self.get_by_chat_id(chat_id)
            
            if user.tokens is None:
                user.tokens = 0
            user.tokens += value
            
            await self.update(user)
        except EntityNotFoundError:
            raise
    
    async def deduct_token_credit(
        self,
        chat_id: str,
        value: int,
    ) -> bool:
    
        try:
            
            user = await self.get_by_chat_id(chat_id)
            
            if user.tokens is not None and user.tokens >= value:
                user.tokens -= value
            else:
                user.tokens = 0
            
            await self.update(user)
        except EntityNotFoundError:
            raise
    
    async def delete_by_id(
        self,
        user_id: str,
    ) -> bool:
    
        try:
            result = await UserCollection.find(
                UserCollection.id == ObjectId(user_id),
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")