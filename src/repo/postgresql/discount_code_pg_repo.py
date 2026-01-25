from src.repo.interface.Idiscount_code_repo import IDiscountCodeRepo
from src.domain.schemas.discount_code.discount_code_model import DiscountCodeModel
from src.infra.database.mongodb.collections.discount_code_collection import DiscountCodeCollection
from bson.objectid import ObjectId
from src.infra.exceptions.exceptions import EntityNotFoundError, InvalidRequestException

class DiscountCodeMongodbRepo(IDiscountCodeRepo):
            
    async def create(
        self,
        discount_code: DiscountCodeModel,
    ) -> DiscountCodeModel:
        
        try:
            await self.get_by_code(discount_code.code)
            raise InvalidRequestException(409, f"Code '{discount_code.code}' already exist")
        except EntityNotFoundError:
            new_discount_code = await DiscountCodeCollection.insert(
                DiscountCodeCollection(**discount_code.model_dump(exclude={"id", "_id"})),
            )
            return DiscountCodeModel.model_validate(new_discount_code, from_attributes=True)
    
    async def get_by_id(
        self,
        discount_code_id: str,
    ) -> DiscountCodeModel:
        
        try:
            code = await DiscountCodeCollection.get(discount_code_id)
            return DiscountCodeModel.model_validate(code, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Code not found")
    
    async def get_by_code(
        self,
        code: str,
    ) -> DiscountCodeModel:
        
        try:
            discount_code = await DiscountCodeCollection.find_one(
                DiscountCodeCollection.code == code.strip(),
            )
            return DiscountCodeModel.model_validate(discount_code, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Code not found")
        
    async def update(
        self,
        discount_code: DiscountCodeModel,
    ) -> bool:
        
        try:                
            to_update: dict = discount_code.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                },
                db_stack="no-sql",
            )
                        
            await DiscountCodeCollection.find_one(
                DiscountCodeCollection.id == discount_code.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id(discount_code.id)
        except:
            raise EntityNotFoundError(status_code=404, message="Code not found")
    
    async def delete_by_id(
        self,
        discount_code_id: str,
    ) -> bool:
        
        try:
            result = await DiscountCodeCollection.find(
                DiscountCodeCollection.id == ObjectId(discount_code_id),
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Code not found")
    
    async def delete_by_code(
        code: str,
    ) -> bool:
        
        try:
            result = await DiscountCodeCollection.find(
                DiscountCodeCollection.code == code.strip(),
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Code not found")