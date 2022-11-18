from patterns import InterfaceService
from repositories.level import CrudLevelRepository
from .entities import LevelRegistration


class LevelRegistrationService(InterfaceService[LevelRegistration]):
    def execute(self, param: LevelRegistration):
        repository: CrudLevelRepository = CrudLevelRepository()

        repository.create(param.departament, param)