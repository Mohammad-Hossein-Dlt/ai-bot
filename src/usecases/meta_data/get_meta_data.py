from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.domain.schemas.meta_data.meta_data_model import MetaDataModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class GetMetaData:
    
    def __init__(
        self,
        meta_data_repo: IMetaDataRepo,
    ):
        
        self.meta_data_repo = meta_data_repo
    
    async def execute(
        self,
    ) -> MetaDataModel:
        
        try:
            return await self.meta_data_repo.get()
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 