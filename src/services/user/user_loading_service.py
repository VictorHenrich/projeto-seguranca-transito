from patterns import InterfaceService, CrudRepository
from repositories.user import CrudUserRepository
from .entities import UserLocation
from models import Usuario




class UserLoadingService(InterfaceService[UserLocation]):
    def execute(self, param: UserLocation) -> Usuario:
        repository: CrudRepository[Usuario] = CrudUserRepository()

        user: Usuario = repository.load(param)

        return user