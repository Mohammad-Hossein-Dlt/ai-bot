# from src.repo.interface.Icache import ICacheRepo
# from src.repo.interface.Iuser_repo import IUserRepo
# from src.models.schemas.bot.callback_request import CallbackDataRequest
# from src.models.schemas.bot.add_credit_request_model import AddCreditRequestModel
# from src.domain.schemas.user.user_model import UserModel
# from typing import ClassVar

# class AddCreditCache:
    
#     step: ClassVar[int] = 1
    
#     def __init__(
#         self,
#         cache_repo: ICacheRepo,
#         user_repo: IUserRepo,
#     ):
        
#         self.cache_repo = cache_repo  
#         self.user_repo = user_repo
            
#     async def execute(
#         self,
#         chat_id: str,
#         callback_data: CallbackDataRequest,
#     ) -> AddCreditRequestModel:
        
#         user: UserModel = await self.user_repo.get_by_chat_id(chat_id)
        
#         cache_id = f"user:{user.id}:{chat_id}:request:{callback_data.message_id}"
#         cache = self.cache_repo.get(cache_id)
        
#         if cache:
#             request: AddCreditRequestModel = AddCreditRequestModel.model_validate(cache)
#         else:
#             request: AddCreditRequestModel = AddCreditRequestModel()
        
#         if callback_data.origin == "t":
#             request.tokens = 
#         elif callback_data.origin == "d":
#             models = self.ai_platforms[request.ai_platform]
#             request.ai_model = models[callback_data.index]

#         return AddCreditRequestModel.model_validate(
#             self.cache_repo.save(
#                 cache_id,
#                 request.model_dump(mode="json"),
#                 60 * 5,
#             ),
#         )
        