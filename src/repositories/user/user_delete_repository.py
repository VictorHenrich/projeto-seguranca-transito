from typing import Protocol
from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindRepository
from models import Usuario
from .user_find_repository import UserFindRepository, UserFindRepositoryParams


class UserDeleteRepositoryParams(Protocol):
    uuid_ser: str


@dataclass
class UserFindProps:
    uuid_user: str


class UserDeleteRepository(BaseRepository):
    def delete(self, params: UserDeleteRepositoryParams) -> None:
        getting_repostiory_param: UserFindRepositoryParams = UserFindProps(
            uuid_user=params.uuid_ser
        )

        getting_repository: IFindRepository[
            UserFindRepositoryParams, Usuario
        ] = UserFindRepository(self.session)

        user: Usuario = getting_repository.get(getting_repostiory_param)

        self.session.delete(user)