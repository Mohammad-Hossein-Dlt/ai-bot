from redis import Redis
from src.repo.interface.Icache import ICacheRepo
import json

class RedisCacheRepo(ICacheRepo):
    
    def __init__(
        self,
        redis_client: Redis,
    ):
        
        self.redis_client = redis_client
        
    def save(
        self,
        chache_id: str,
        data: dict,
        ttl: int,
    ) -> dict:
                
        self.redis_client.execute_command(
            "JSON.SET",
            chache_id,
            ".",
            json.dumps(data),
        )
                
        self.redis_client.expire(
            chache_id,
            ttl,
        )
                                                
        return data

    def get(
        self,
        chache_id: str,
    ) -> dict | None:
        
        try:

            cached = self.redis_client.execute_command(
                "JSON.GET",
                chache_id,
            )
            return json.loads(cached)
        
        except:
            return None
        
    def delete(
        self,
        chache_id: str,
    ) -> dict | None:
        
        try:

            self.redis_client.unlink(chache_id)
            return True
        except:
            return False
        
# from redis import Redis
# from src.repo.interface.Icache import ICacheRepo
# from pydantic import BaseModel
# from typing import TypeVar, Generic, Type

# T = TypeVar("T", bound=BaseModel)

# class CacheRedisRepo(ICacheRepo, Generic[T]):
    
#     def __init__(
#         self,
#         redis_client: Redis,
#     ):
        
#         self.redis_client = redis_client
        
#     def save_user_request(
#         self,
#         request_id: str,
#         request: T,
#     ) -> T:
                
#         self.redis_client.execute_command(
#             "JSON.SET",
#             request_id,
#             ".",
#             request.model_dump_json(),
#         )
                
#         self.redis_client.expire(
#             request_id,
#             1 * 60,
#         )
                                                
#         return request

#     def get_user_request(
#         self,
#         request_id: str,
#         model: Type[T],
#     ) -> T | None:
        
#         try:

#             cached_request = self.redis_client.execute_command(
#                 "JSON.GET",
#                 request_id,
#             )
#             return model.model_validate_json(cached_request)
        
#         except:
#             return None