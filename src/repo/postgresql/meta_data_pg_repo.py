from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.domain.schemas.meta_data.meta_data_model import MetaDataModel
from src.infra.database.mongodb.collections.meta_data_collection import MetaDataCollection
from src.infra.exceptions.exceptions import EntityNotFoundError, InvalidRequestException

class MetaDataMongodbRepo(IMetaDataRepo):
    
    async def create(
        self,
        meta_data: MetaDataModel,
    ) -> MetaDataModel:

        try:
            await self.get()
            raise InvalidRequestException(409, f"Meta data already exist")
        except EntityNotFoundError:
            new_meta_data = await MetaDataCollection.insert(
                MetaDataCollection(**meta_data.model_dump(exclude={"id", "_id"})),
            )
            return MetaDataModel.model_validate(new_meta_data, from_attributes=True)
    
    async def get(
        self,
    ) -> MetaDataModel:
    
        try:
            meta_data = await MetaDataCollection.find().first_or_none()
            return MetaDataModel.model_validate(meta_data, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Meta Data not found")
    
    async def update(
        self,
        meta_data: MetaDataModel,
    ) -> bool:
    
        try:                
            to_update: dict = meta_data.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                },
                db_stack="no-sql",
            )
                        
            pre_meta_data: MetaDataCollection = await MetaDataCollection.find().first_or_none()()
            
            await pre_meta_data.update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get()
        except:
            raise EntityNotFoundError(status_code=404, message="Meta Data not found")
    
    async def delete(
        self,
    ) -> bool:
    
        try:
            result = await MetaDataCollection.delete_all()
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Meta Data not found")