from ._router import router
from fastapi import Depends, Query, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.models.schemas.meta_data.update_meta_data_input import UpdateMetaDataInput
from src.usecases.meta_data.update_meta_data import UpdateMetaData
from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.routes.depends.repo_depend import meta_data_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.put(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def update_meta_data(
    meta_data: UpdateMetaDataInput = Query(...),
    meta_data_repo: IMetaDataRepo = Depends(meta_data_repo_depend),
):
    try:
        update_meta_data_usecase = UpdateMetaData(meta_data_repo)
        output = await update_meta_data_usecase.execute(meta_data)
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
