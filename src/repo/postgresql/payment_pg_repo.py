from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.domain.schemas.payment.payment_model import PaymentModel
from src.infra.database.mongodb.collections.payment_collection import PaymentCollection
from bson.objectid import ObjectId
from src.infra.exceptions.exceptions import EntityNotFoundError, InvalidRequestException

class PaymentMongodbRepo(IPaymentRepo):
    
    async def create(
        self,
        payment: PaymentModel,
    ) -> PaymentModel:

        try:
            await self.get_by_id(payment.id)
            raise InvalidRequestException(409, f"Payment already exist")
        except EntityNotFoundError:
            new_meta_data = await PaymentCollection.insert(
                PaymentCollection(**payment.model_dump(exclude={"id", "_id"})),
            )
            return PaymentModel.model_validate(new_meta_data, from_attributes=True)
    
    async def get_by_id(
        self,
        payment_id: str,
    ) -> PaymentModel:
    
        try:
            code = await PaymentCollection.get(payment_id)
            return PaymentModel.model_validate(code, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Code not found")
        
    async def get_by_(
        self,
    ) -> PaymentModel:
    
        raise NotImplementedError
    
    async def modify(
        self,
        payment: PaymentModel,
    ) -> bool:
    
        try:                
            to_update: dict = payment.custom_model_dump(
                exclude_unset=True,
                exclude_none=True,
                exclude={
                    "id",
                },
                db_stack="no-sql",
            )
                        
            await PaymentCollection.find_one(
                PaymentCollection.id == PaymentMongodbRepo.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id(payment.id)
        except:
            raise EntityNotFoundError(status_code=404, message="Order not found")

    async def delete_by_id(
        self,
        payment_id: str,
    ) -> bool:
    
        try:
            result = await PaymentCollection.find(
                PaymentCollection.id == ObjectId(payment_id),
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Code not found")
    
    async def delete_by_(
        self,
    ) -> bool:
    
        raise NotImplementedError