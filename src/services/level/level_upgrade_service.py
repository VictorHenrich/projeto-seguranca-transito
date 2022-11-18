from patterns import InterfaceService
from repositories.level import CrudLevelRepository
from .entities import LevelRegistration


class LevelUpgradeService(InterfaceService[LevelRegistration]):
    def execute(self, param: LevelRegistration):
        repository: CrudLevelRepository = CrudLevelRepository()

        repository.update()