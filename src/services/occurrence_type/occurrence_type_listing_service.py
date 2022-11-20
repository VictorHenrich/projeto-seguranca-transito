from patterns import CrudRepository, InterfaceService
from models import TipoOcorrencia
from repositories.occurrence_type import CrudOccurrenceTypeRepository
from .entities import OccurrenceTypeListingLocation


class OccurrenceTypeListingService(InterfaceService[OccurrenceTypeListingLocation]):
    def execute(self, param: OccurrenceTypeListingLocation) -> TipoOcorrencia:
        repository: CrudRepository[TipoOcorrencia] = CrudOccurrenceTypeRepository()

        occurrences_types: list[TipoOcorrencia] = repository.fetch(param)

        return occurrences_types