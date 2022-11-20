from patterns import CrudRepository, InterfaceService
from models import TipoOcorrencia
from repositories.occurrence_type import CrudOccurrenceTypeRepository
from .entities import OccurrenceTypeRegistration


class OccurrenceTypeCriationService(InterfaceService[OccurrenceTypeRegistration]):
    def execute(self, param: OccurrenceTypeRegistration) -> None:
        repository: CrudRepository[TipoOcorrencia] = CrudOccurrenceTypeRepository()

        repository.create(param)