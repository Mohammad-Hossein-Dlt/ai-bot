from src.repo.interface.Itoken_settings_repo import ITokenSettingsRepo
from src.domain.schemas.token_settings.token_settings_model import TokenSettingsModel
from src.infra.database.mongodb.collections.token_settings_collection import TokenSettingsCollection
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError

class TokenSettingsMongodbRepo(ITokenSettingsRepo):
            
    async def create(
        self,
        token_settings: TokenSettingsModel,
    ) -> TokenSettingsModel:

        try:
            await self.get()
            raise DuplicateEntityError(409, f"Token Settings already exist")
        except EntityNotFoundError:
            new_meta_data = await TokenSettingsCollection.insert(
                TokenSettingsCollection(**token_settings.model_dump(exclude={"id", "_id"})),
            )
            return TokenSettingsModel.model_validate(new_meta_data, from_attributes=True)
    
    async def get(
        self,
    ) -> TokenSettingsModel:
    
        try:
            meta_data = await TokenSettingsCollection.find().first_or_none()
            return TokenSettingsModel.model_validate(meta_data, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Token Settings not found")
    
    async def update(
        self,
        token_settings: TokenSettingsModel,
    ) -> TokenSettingsModel:
    
        try:                
            to_update: dict = token_settings.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                },
                db_stack="no-sql",
            )
                        
            pre_meta_data: TokenSettingsCollection = await TokenSettingsCollection.find().first_or_none()
            
            await pre_meta_data.update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get()
        except:
            raise EntityNotFoundError(status_code=404, message="Token Settings not found")
    
    async def delete(
        self,
    ) -> bool:
    
        try:
            result = await TokenSettingsCollection.delete_all()
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Token Settings not found")