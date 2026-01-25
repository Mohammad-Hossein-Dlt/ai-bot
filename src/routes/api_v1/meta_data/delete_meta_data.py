from ._router import router
from fastapi import Depends, HTTPException
from src.routes.http_response.responses import ResponseMessage
from src.usecases.meta_data.delete_meta_data import DeleteMetaData
from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.routes.depends.repo_depend import meta_data_repo_depend
from src.infra.exceptions.exceptions import AppBaseException

@router.delete(
    "/",
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }    
)
async def delete_meta_data(
    meta_data_repo: IMetaDataRepo = Depends(meta_data_repo_depend),
):
    try:
        delete_meta_data_usecase = DeleteMetaData(meta_data_repo)
        output = await delete_meta_data_usecase.execute()
        return output.model_dump(mode="json")
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=str(ex))
