from abc import ABC, abstractmethod

class ICacheRepo(ABC):
    
    @abstractmethod
    def save(
        cache_id: str,
        data: dict,
        ttl: int,
    ) -> dict:
        
        raise NotImplementedError
    
    @abstractmethod
    def get(
        chache_id: str,
    ) -> dict | None:
        
        raise NotImplementedError
    
# from abc import ABC, abstractmethod
# from pydantic import BaseModel
# from typing import TypeVar, Generic

# T = TypeVar("T", bound=BaseModel)

# class ICacheRepo(ABC, Generic[T]):
    
#     @abstractmethod
#     def save_user_request(
#         request_id: str,
#         request: T,
#     ) -> T:
        
#         raise NotImplementedError
    
#     @abstractmethod
#     def get_user_request(
#         request_id: str,
#         model: T,
#     ) -> T | None:
        
#         raise NotImplementedError