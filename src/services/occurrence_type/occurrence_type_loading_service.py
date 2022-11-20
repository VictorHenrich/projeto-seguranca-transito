from patterns import CrudRepository, InterfaceService
from models import TipoOcorrencia
from repositories.occurrence_type import CrudOccurrenceTypeRepository
from .entities import OccurrenceTypeLocation


class OccurrenceTypeLoadingService(InterfaceService[OccurrenceTypeLocation]):
    def execute(self, param: OccurrenceTypeLocation) -> TipoOcorrencia:
        repository: CrudRepository[TipoOcorrencia] = CrudOccurrenceTypeRepository()

        occurrence_type: TipoOcorrencia = repository.load(param)

        return occurrence_type