from patterns import InterfaceService, CrudRepository
from repositories.departament_user import CrudDepartamentUserRepository
from .entities import DepartamentUserRegistration


class DepartamentUserCriationService(InterfaceService[DepartamentUserRegistration]):
    def execute(self, param: DepartamentUserRegistration) -> None:
        
        repository: CrudRepository = CrudDepartamentUserRepository()

        repository.create(param)