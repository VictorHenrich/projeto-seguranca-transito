from patterns import InterfaceService
from .entities import LevelLocation
from repositories.level import CrudLevelRepository



class LevelExclusionService(InterfaceService[LevelLocation]):
    def execute(self, param: LevelLocation) -> None:
        repository: CrudLevelRepository = CrudLevelRepository()

        repository.delete(param)