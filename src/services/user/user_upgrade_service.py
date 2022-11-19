from patterns import InterfaceService, CrudRepository
from repositories.user import CrudUserRepository
from .entities import UserUpgrade
from models import Usuario




class UserUpgradeService(InterfaceService[UserUpgrade]):
    def execute(self, param: UserUpgrade) -> None:
        repository: CrudRepository[Usuario] = CrudUserRepository()

        repository.update(param.location_data, param.data)