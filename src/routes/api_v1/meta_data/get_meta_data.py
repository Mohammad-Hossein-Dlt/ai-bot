from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.meta_data.get_meta_data import GetMetaData
from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.routes.depends.repo_depend import meta_data_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.get(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def get_meta_data(
    meta_data_repo: IMetaDataRepo = Depends(meta_data_repo_depend),
):
    try:
        get_meta_data_usecase = GetMetaData(meta_data_repo)
        output = await get_meta_data_usecase.execute()
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
