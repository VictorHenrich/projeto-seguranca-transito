from patterns import InterfaceService, CrudRepository
from .entities import LevelLocation
from models import Nivel
from repositories.level import CrudLevelRepository



class LevelListingService(InterfaceService[LevelLocation]):
    def execute(self, param: LevelLocation) -> list[Nivel]:
        repository: CrudRepository[Nivel] = CrudLevelRepository()

        levels: list[Nivel] = repository.fetch(param)

        return levels