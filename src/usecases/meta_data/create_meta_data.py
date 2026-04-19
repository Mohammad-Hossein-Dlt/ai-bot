from src.repo.interface.Imeta_data_repo import IMetaDataRepo
from src.models.schemas.meta_data.create_meta_data_input import CreateMetaDataInput
from src.domain.schemas.meta_data.meta_data_model import MetaDataModel
from src.infra.exceptions.exceptions import AppBaseException, OperationFailureException

class CreateMetaData:
    
    def __init__(
        self,
        meta_data_repo: IMetaDataRepo,
    ):
        
        self.meta_data_repo = meta_data_repo
    
    async def execute(
        self,
        new_meta_data: CreateMetaDataInput,
    ) -> MetaDataModel:
        
        try:
            to_create: MetaDataModel = MetaDataModel.model_validate(new_meta_data, from_attributes=True)
            return await self.meta_data_repo.create(to_create)
        except AppBaseException:
            raise
        except:
            raise OperationFailureException(500, "Internal server error") 