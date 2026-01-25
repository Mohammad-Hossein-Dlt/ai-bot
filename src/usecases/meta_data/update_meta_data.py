from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.models.schemas.meta_data.update_meta_data_input import UpdateMetaDataInput
from src.domain.schemas.meta_data.meta_data_model import MetaDataModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class UpdateMetaData:
    
    def __init__(
        self,
        meta_data_repo: IMetaDataRepo,
    ):
        
        self.meta_data_repo = meta_data_repo
    
    async def execute(
        self,
        meta_data: UpdateMetaDataInput,
    ) -> MetaDataModel:
        
        try:
            to_update: MetaDataModel = MetaDataModel.model_validate(meta_data, from_attributes=True)
            return await self.meta_data_repo.update(to_update)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 