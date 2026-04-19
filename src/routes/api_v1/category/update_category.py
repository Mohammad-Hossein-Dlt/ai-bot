from ._router import router
from fastapi import Query, Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.category.update_category_input import UpdateCategoryInput
from src.usecases.category.update_category import UpdateCategory
from src.repo.interface.Icategory_repo import ICategoryRepo
from src.routes.depends.repo_depend import category_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def update_one_category(
    category: UpdateCategoryInput = Query(...),
    category_repo: ICategoryRepo = Depends(category_repo_depend),
):
    try:
        update_category_usecase = UpdateCategory(category_repo)
        output = await update_category_usecase.execute(category)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
