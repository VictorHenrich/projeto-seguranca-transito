from patterns import InterfaceService, CrudRepository
from repositories.departament_user import CrudDepartamentUserRepository
from .entities import DepartamentUserLocation
from models import UsuarioDepartamento


class DepartamentUserLoadingService(InterfaceService[DepartamentUserLocation]):
    def execute(self, param: DepartamentUserLocation) -> UsuarioDepartamento:
        repository: CrudRepository = CrudDepartamentUserRepository()

        user: UsuarioDepartamento = repository.load(param)

        return user