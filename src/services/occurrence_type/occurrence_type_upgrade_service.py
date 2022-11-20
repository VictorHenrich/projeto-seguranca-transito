from patterns import CrudRepository, InterfaceService
from models import TipoOcorrencia
from repositories.occurrence_type import CrudOccurrenceTypeRepository
from .entities import OccurrenceTypeUpgrade


class OccurrenceTypeUpgradeService(InterfaceService[OccurrenceTypeUpgrade]):
    def execute(self, param: OccurrenceTypeUpgrade) -> None:
        repository: CrudRepository[TipoOcorrencia] = CrudOccurrenceTypeRepository()

        repository.update(param.location_data, param.data)