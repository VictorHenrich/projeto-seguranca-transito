from dataclasses import dataclass

from patterns.repository import BaseRepository, IGettingRepository
from models import Usuario
from .user_getting_repository import (
    UserGettingRepository,
    UserGettingRepositoryParam
)



@dataclass
class UserExclusionRepositoryParam:
    uuid_ser: str


class UserExclusionRepository(BaseRepository):
    def delete(self, param: UserExclusionRepositoryParam) -> None:
        getting_repostiory_param: UserGettingRepositoryParam = \
            UserGettingRepositoryParam(
                uuid_user=param.uuid_ser
            )

        getting_repository: IGettingRepository[UserGettingRepositoryParam, Usuario] = \
            UserGettingRepository(self.session)

        user: Usuario = getting_repository.get(getting_repostiory_param)

        self.session.delete(user)
