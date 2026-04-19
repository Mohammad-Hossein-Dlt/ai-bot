from src.repo.interface.Icategory_repo import ICategoryRepo
from src.models.schemas.category.update_category_input import UpdateCategoryInput
from src.domain.schemas.category.category_model import CategoryModel
from src.infra.exceptions.exceptions import AppBaseException, EntityNotFoundError, InvalidRequestException, OperationFailureException

class UpdateCategory:
    
    def __init__(
        self,
        category_repo: ICategoryRepo,
    ):        
        self.category_repo = category_repo  
    
    async def execute(
        self,
        category: UpdateCategoryInput,
    ) -> CategoryModel:
        
        if category.parent_id and category.parent_id != category.id:
            try:
                parent: CategoryModel = await self.category_repo.get_category_by_id(category.parent_id)
                category.parent_id = parent.id
            except EntityNotFoundError as ex:
                raise EntityNotFoundError(ex.status_code, "Parent not found")
        elif category.parent_id == category.id:
                raise InvalidRequestException(400, "Parent-id cannot be equal to id")
                
        try:
            to_update = CategoryModel.model_validate(category, from_attributes=True)
            return await self.category_repo.update_category(to_update)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error")