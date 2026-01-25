from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.domain.schemas.user.account_model import AccountModel
from src.infra.database.mongodb.collections.user_collection import UserCollection
from bson.objectid import ObjectId
from beanie.operators import In
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError

class UserMongodbRepo(IUserRepo):
            
    async def create(
        self,
        user: UserModel,
    ) -> UserModel:
        
        try:
            await self.get_by_chat_id(*user.platform_accounts)
            raise DuplicateEntityError(409, "User already exist")
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
        *args: AccountModel | str | int,
    ) -> UserModel:
    
        try:
            chat_ids = [arg.chat_id if isinstance(arg, AccountModel) else str(arg) for arg in args]
            user = await UserCollection.find_one(
                In(UserCollection.platform_accounts.chat_id, chat_ids),
            )
            return UserModel.model_validate(user, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def update(
        self,
        user: UserModel,
    ) -> UserModel:
        
        try:                
            to_update: dict = user.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                    "tokens",
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
                        
            return await self.get_by_chat_id(user.platform_accounts)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def modify_token_credit(
        self,
        chat_id: str,
        value: int,
    ) -> UserModel:
    
        try: 
            
            await UserCollection.find_one(
                # In(UserCollection.platform_accounts.chat_id, [chat_id]),
                UserCollection.platform_accounts.chat_id == chat_id,
            ).update_one(
                [
                    {
                        "$set": {
                            UserCollection.tokens: {
                                "$max": [0, {"$add": ["$tokens", value]}],
                            },
                        },
                    },
                ],
            )
            
            return await self.get_by_chat_id(chat_id)
        
        except EntityNotFoundError:
            raise
        
    async def modify_token_credit_for_all_users(
        self,
        value: int,
    ) -> bool:
    
        try: 
            result = await UserCollection.find().update_many(
                [
                    {
                        "$set": {
                            UserCollection.tokens: {
                                "$max": [0, {"$add": ["$tokens", value]}],
                            },
                        },
                    },
                ],
            )
            
            return bool(result.modified_count)
        
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
        
    async def delete_by_chat_id(
        self,
        chat_id: str,
    ) -> bool:
    
        try:
            result = await UserCollection.find(
                # In(UserCollection.platform_accounts.chat_id, [chat_id]),
                UserCollection.platform_accounts.chat_id == chat_id,
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")