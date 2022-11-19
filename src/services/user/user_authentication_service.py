from patterns import InterfaceService, AuthRepository
from repositories.user import AuthUserRepository
from .entities import UserAuthentication
from models import Usuario




class UserAuthenticationService(InterfaceService[UserAuthentication]):
    def execute(self, param: UserAuthentication) -> Usuario:
        repository: AuthRepository[Usuario] = AuthUserRepository()

        user: Usuario = repository.auth(param)

        return user