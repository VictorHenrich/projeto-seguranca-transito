from patterns import InterfaceService, CrudRepository
from repositories.departament_user import CrudDepartamentUserRepository
from .entities import DepartamentUserUpgrade


class DepartamentUserUpgradeService(InterfaceService[DepartamentUserUpgrade]):
    def execute(self, param: DepartamentUserUpgrade) -> None:
        repository: CrudRepository = CrudDepartamentUserRepository()

        repository.update(param.location_data, param.data)