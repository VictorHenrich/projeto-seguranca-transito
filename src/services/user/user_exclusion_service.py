from patterns import InterfaceService, CrudRepository
from repositories.user import CrudUserRepository
from .entities import UserLocation
from models import Usuario




class UserExclusionService(InterfaceService[UserLocation]):
    def execute(self, param: UserLocation) -> None:
        repository: CrudRepository[Usuario] = CrudUserRepository()

        repository.delete(param)