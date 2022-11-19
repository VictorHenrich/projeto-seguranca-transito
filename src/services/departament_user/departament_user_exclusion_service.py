from patterns import InterfaceService, CrudRepository
from repositories.departament_user import CrudDepartamentUserRepository
from .entities import DepartamentUserLocation
from models import UsuarioDepartamento


class DepartamentUserExclusionService(InterfaceService[DepartamentUserLocation]):
    def execute(self, param: DepartamentUserLocation) -> list[UsuarioDepartamento]:
        repository: CrudRepository = CrudDepartamentUserRepository()

        repository.delete(param)