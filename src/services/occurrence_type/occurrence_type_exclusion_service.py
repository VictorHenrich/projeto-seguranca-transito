from patterns import CrudRepository, InterfaceService
from models import TipoOcorrencia
from repositories.occurrence_type import CrudOccurrenceTypeRepository
from .entities import OccurrenceTypeLocation


class OccurrenceTypeExclusionService(InterfaceService[OccurrenceTypeLocation]):
    def execute(self, param: OccurrenceTypeLocation) -> None:
        repository: CrudRepository[TipoOcorrencia] = CrudOccurrenceTypeRepository()

        repository.delete(param)