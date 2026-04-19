from abc import ABC, abstractmethod
from src.domain.schemas.category.category_model import CategoryModel
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput

class ICategoryRepo(ABC):
        
    @abstractmethod
    async def insert_category(
        category: CategoryModel,
    ) -> CategoryModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_categories_with_filter(
        filter: CategoryFilterInput,
    ) ->  list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_child_to_parent(
        filter: CategoryFilterInput,
    ) ->  list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_parent_to_child(
        filter: CategoryFilterInput,
    ) -> list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_categories_with_parent_id(
        parent_id: str | None,    
    ) ->  list[CategoryModel]:
    
        raise NotImplementedError
    
    @abstractmethod
    async def get_category_by_id(
        category_id: str,
    ) ->  CategoryModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def update_category(
        category: CategoryModel,
    ) ->  CategoryModel:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_all_categories() -> bool:
    
        raise NotImplementedError
    
    @abstractmethod
    async def delete_category(
        category_id: str,
    ) -> bool:
    
        raise NotImplementedError