from patterns import InterfaceService, CrudRepository
from repositories.departament import CrudDepartamentRepository
from .entities import DepartamentLocation
from models import Departamento


class DepartamentLoadingService(InterfaceService[DepartamentLocation]):
    def execute(self, param: DepartamentLocation) -> Departamento:
        repository: CrudRepository[Departamento] = CrudDepartamentRepository()

        departament: Departamento = repository.load(param)

        return departament