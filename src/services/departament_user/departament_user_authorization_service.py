from typing import Tuple

from patterns import InterfaceService, AuthRepository
from repositories.departament_user import AuthDepartamentUserRepository
from .entities import DepartamentUserAuthorization
from models import UsuarioDepartamento, Departamento


class DepartamentUserAuthorizationService(InterfaceService[DepartamentUserAuthorization]):
    def execute(self, param: DepartamentUserAuthorization) -> Tuple[Departamento, UsuarioDepartamento]:
        repository: AuthRepository = AuthDepartamentUserRepository()

        return repository.auth(param)