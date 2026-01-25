from src.repo.interface.Ibot_settings_repo import IBotSettingsRepo
from src.domain.schemas.bot_settings.bot_settings_model import BotSettingsModel
from src.infra.database.mongodb.collections.bot_settings_collection import BotSettingsCollection
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError

class BotSettingsMongodbRepo(IBotSettingsRepo):
    
    async def create(
        self,
        settings: BotSettingsModel,
    ) -> BotSettingsModel:

        try:
            await self.get()
            raise DuplicateEntityError(409, f"Settings already exist")
        except EntityNotFoundError:
            new_meta_data = await BotSettingsCollection.insert(
                BotSettingsCollection(**settings.model_dump(exclude={"id", "_id"})),
            )
            return BotSettingsModel.model_validate(new_meta_data, from_attributes=True)
    
    async def get(
        self,
    ) -> BotSettingsModel:
    
        try:
            meta_data = await BotSettingsCollection.find().first_or_none()
            return BotSettingsModel.model_validate(meta_data, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Settings not found")
    
    async def update(
        self,
        settings: BotSettingsModel,
    ) -> BotSettingsModel:
    
        try:                
            to_update: dict = settings.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                },
                db_stack="no-sql",
            )
                        
            pre_meta_data: BotSettingsCollection = await BotSettingsCollection.find().first_or_none()
            
            await pre_meta_data.update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get()
        except:
            raise EntityNotFoundError(status_code=404, message="Settings not found")
    
    async def delete(
        self,
    ) -> bool:
    
        try:
            result = await BotSettingsCollection.delete_all()
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Settings not found")