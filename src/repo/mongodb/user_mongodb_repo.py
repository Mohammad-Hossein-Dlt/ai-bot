from src.repo.interface.Iuser_repo import IUserRepo
from src.domain.schemas.user.user_model import UserModel
from src.infra.database.mongodb.collections.user_collection import UserCollection
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError
from bson.objectid import ObjectId
from beanie.operators import And

class UserMongodbRepo(IUserRepo):
    
    def __init__(
        self,
        bot_platform: str | None = None,
    ):
        self.bot_platform = bot_platform
        
            
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
        chat_id: int | str,
        bot_platform: str | None = None,
    ) -> UserModel:
    
        try:
            if isinstance(chat_id, int):
                chat_id = str(chat_id)
            
            user = await UserCollection.find_one(
                And(
                    UserCollection.platform_accounts.chat_id == chat_id,
                    UserCollection.platform_accounts.platform == (bot_platform or self.bot_platform),
                ),
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
            
            return await self.get_by_id(user.id)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")
    
    async def modify_token_credit(
        self,
        user: UserModel,
        value: int,
    ) -> UserModel:
    
        try:
            
            to_update = [
                {
                    "$set": {
                        UserCollection.tokens: {
                            "$max": [0, {"$add": ["$tokens", value]}],
                        },
                    },
                },
            ]
            
            await UserCollection.find_one(UserCollection.id == user.id).update_one(to_update)
            
            return await self.get_by_id(user.id)
        
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
        chat_id: int | str,
        bot_platform: str,
    ) -> bool:
    
        try:
            
            if isinstance(chat_id, int):
                chat_id = str(chat_id)
            
            result = await UserCollection.find(
                And(
                    UserCollection.platform_accounts.chat_id == chat_id,
                    UserCollection.platform_accounts.platform == (bot_platform or self.bot_platform),
                ),
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="User not found")