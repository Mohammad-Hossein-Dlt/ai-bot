from src.repo.interface.Ipayment_repo import IPaymentRepo
from src.domain.schemas.payment.payment_model import PaymentModel
from src.infra.database.mongodb.collections.payment_collection import PaymentCollection
from bson.objectid import ObjectId
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError

class PaymentMongodbRepo(IPaymentRepo):
    
    async def create(
        self,
        payment: PaymentModel,
    ) -> PaymentModel:

        try:
            await self.get_by_id(payment.id)
            raise DuplicateEntityError(409, f"Payment already exist")
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
            payment = await PaymentCollection.get(payment_id)
            return PaymentModel.model_validate(payment, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Payment not found")
        
    async def get_all_by_user_id(
        self,
        user_id: str,
    ) -> list[PaymentModel]:
    
        try:
            payments = await PaymentCollection.find(
                PaymentCollection.user_id == ObjectId(user_id),
            ).to_list()
            return [ PaymentModel.model_validate(p, from_attributes=True) for p in payments ]
        except:
            raise EntityNotFoundError(status_code=404, message="Payment not found")
    
    async def modify(
        self,
        payment: PaymentModel,
    ) -> PaymentModel:
    
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
                PaymentCollection.id == payment.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_by_id(payment.id)
        except:
            raise EntityNotFoundError(status_code=404, message="Payment not found")

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
            raise EntityNotFoundError(status_code=404, message="Payment not found")
    
    async def delete_by_user_id(
        self,
        user_id: str,
    ) -> bool:
        
        try:
            result = await PaymentCollection.find(
                PaymentCollection.user_id == ObjectId(user_id),
            ).delete()
            
            return bool(result.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Payment not found")