from patterns import InterfaceService, CrudRepository
from repositories.departament_user import CrudDepartamentUserRepository
from .entities import DepartamentUserLocation
from models import UsuarioDepartamento


class DepartamentUserListingService(InterfaceService[DepartamentUserLocation]):
    def execute(self, param: DepartamentUserLocation) -> list[UsuarioDepartamento]:
        repository: CrudRepository = CrudDepartamentUserRepository()

        users: list[UsuarioDepartamento] = repository.fetch(param)

        return users