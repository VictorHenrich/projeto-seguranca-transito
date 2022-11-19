from patterns import InterfaceService, CrudRepository
from repositories.user import CrudUserRepository
from .entities import UserRegistration
from models import Usuario




class UserCriationService(InterfaceService[UserRegistration]):
    def execute(self, param: UserRegistration) -> None:
        repository: CrudRepository[Usuario] = CrudUserRepository()

        repository.create(param)