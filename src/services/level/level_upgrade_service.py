from dataclasses import dataclass

from patterns import InterfaceService
from repositories.level import CrudLevelRepository
from .entities import LevelUpdate






class LevelUpgradeService(InterfaceService[LevelUpdate]):
    def execute(self, param: LevelUpdate):
        repository: CrudLevelRepository = CrudLevelRepository()

        repository.update(param.location_data, param.data)