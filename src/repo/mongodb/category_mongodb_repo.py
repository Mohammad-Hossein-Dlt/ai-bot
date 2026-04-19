from src.repo.interface.Icategory_repo import ICategoryRepo
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.database.mongodb.collections.category_collection import CategoryCollection
from src.models.schemas.filter.categories_filter_input import CategoryFilterInput
from src.infra.exceptions.exceptions import EntityNotFoundError, DuplicateEntityError
from src.infra.utils.convert_id import convert_object_id

from beanie.operators import And

class CategoryMongodbRepo(ICategoryRepo):
        
    async def insert_category(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        
        try:
            await self.check_category(category)
            raise DuplicateEntityError(409, "Category already exist")
        except EntityNotFoundError:
            new_category = await CategoryCollection.insert(
                CategoryCollection(**category.model_dump(exclude={"id", "_id"})),
            )
            return CategoryModel.model_validate(new_category, from_attributes=True)
    
    async def check_category(
        self,
        category: CategoryModel,
    ) -> CategoryModel:
        
        try:
            result = await CategoryCollection.find_one(
                And(
                    CategoryCollection.ai_action_type == category.ai_action_type,
                    CategoryCollection.ai_platform_type == category.ai_platform_type,
                    CategoryCollection.slug == category.slug,                    
                ),
            )
            return CategoryModel.model_validate(result, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def get_categories_with_filter(
        self,
        filter: CategoryFilterInput,
    ) ->  list[CategoryModel]:
        
        try:
            if filter.based_on == "parent-id":
                return await self.get_parent_to_child(filter)
            elif filter.based_on == "child-to-parent":
                return await self.get_child_to_parent(filter)
        except EntityNotFoundError:
            raise EntityNotFoundError(status_code=404, message="There are no categories")
        
    async def get_child_to_parent(
        self,
        filter: CategoryFilterInput,
    ) ->  list[CategoryModel]:
        
        async def get_parent(
            parent_id: str | None = None,
        ) -> CategoryModel | None:
            try:
                return await self.get_category_by_id(parent_id, filter.ai_action_type, filter.ai_platform_type)
            except:
                return None
        
        async def get_categories(
            category: CategoryModel = None,
        ) -> list[CategoryModel]:
                                 
            result: list[CategoryModel] = []
            
            if not category:
                category = await get_parent(filter.id)
            
            if not category:
                return result    
                        
            result.append(category)
                            
            parent = await get_parent(category.parent_id)

            if parent and parent.parent_id:
                result.extend( await get_categories(parent) )
                return result
            elif parent:
                result.append(parent)
                return result
            else:
                return result
                
        categories = await get_categories()
        categories.reverse()
        
        return categories
    
    async def get_parent_to_child(
        self,
        filter: CategoryFilterInput,
    ) -> list[CategoryModel]:
        
        parents_list = await self.get_categories_with_parent_id(filter.id, filter.ai_action_type, filter.ai_platform_type)
            
        for parent in parents_list:
            children = await self.get_categories_with_parent_id(parent.id)
            
            if children:
                setattr(parent, "children", children)
                
        return parents_list
                    
    async def get_categories_with_parent_id(
        self,
        parent_id: str,
        ai_action_type: str | None = None,
        ai_platform_type: str | None = None,
    ) -> list[CategoryModel]:

        parent_id = convert_object_id(parent_id)
        
        if ai_action_type and ai_platform_type:
                    
            categories_list = await CategoryCollection.find_many(
                And(
                    CategoryCollection.parent_id == parent_id,
                    CategoryCollection.ai_action_type == ai_action_type,
                    CategoryCollection.ai_platform_type == ai_platform_type,
                ),
            ).to_list()
            
        elif ai_action_type:
            
            categories_list = await CategoryCollection.find_many(
                And(
                    CategoryCollection.parent_id == parent_id,
                    CategoryCollection.ai_action_type == ai_action_type,
                ),
            ).to_list()
        
        elif ai_platform_type:
            
            categories_list = await CategoryCollection.find_many(
                And(
                    CategoryCollection.parent_id == parent_id,
                    CategoryCollection.ai_platform_type == ai_platform_type,
                ),
            ).to_list()
            
        else:

            categories_list = await CategoryCollection.find_many(
                CategoryCollection.parent_id == parent_id,
            ).to_list()
        
        return [ CategoryModel.model_validate(category, from_attributes=True) for category in categories_list ]
    
    async def get_category_by_id(
        self,
        category_id: str,
        ai_action_type: str | None = None,
        ai_platform_type: str | None = None,
    ) ->  CategoryModel:
        
        try:
                                    
            category_id = convert_object_id(category_id)
            
            if ai_action_type and ai_platform_type:
                                
                category = await CategoryCollection.find_one(
                    And(
                        CategoryCollection.id == category_id,
                        CategoryCollection.ai_action_type == ai_action_type,
                        CategoryCollection.ai_platform_type == ai_platform_type,
                    ),
                )

            elif ai_action_type:

                category = await CategoryCollection.find_one(
                    And(
                        CategoryCollection.id == category_id,
                        CategoryCollection.ai_action_type == ai_action_type,
                    ),
                )
            
            elif ai_platform_type:
                
                category = await CategoryCollection.find_one(
                    And(
                        CategoryCollection.id == category_id,
                        CategoryCollection.ai_platform_type == ai_platform_type,
                    ),
                )
            
            else:
                
                category = await CategoryCollection.find_one(
                    CategoryCollection.id == category_id,
                )
                        
            return CategoryModel.model_validate(category, from_attributes=True)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
    
    async def update_category(
        self,
        category: CategoryModel,
    ) ->  CategoryModel:
        
        try:               
            
            to_update: dict = category.custom_model_dump(
                exclude_unset=True,
                exclude={
                    "id",
                },
                db_stack="no-sql",
            )
            
            await CategoryCollection.find(
                CategoryCollection.id == category.id,
            ).update(
                {
                    "$set": to_update,
                },
            )
                        
            return await self.get_category_by_id(category.id)
        except EntityNotFoundError:
            raise
    
    async def delete_all_categories(
        self,
    ) -> bool:
        try:
            delete_categories = await CategoryCollection.delete_all()
            return bool(delete_categories.deleted_count) 
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")
        
    async def delete_category(
        self,
        category_id: str,
    ) -> bool:
        
        try:
            category_id = convert_object_id(category_id)
            delete_category = await CategoryCollection.find(
                CategoryCollection.id == category_id,
            ).delete()                       
            return bool(delete_category.deleted_count)
        except:
            raise EntityNotFoundError(status_code=404, message="Category not found")