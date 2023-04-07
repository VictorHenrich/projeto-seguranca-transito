from typing import Protocol

from patterns.repository import BaseRepository, IFindRepository
from models import User
from .user_find_repository import UserFindRepository, UserFindRepositoryParams


class UserDeleteRepositoryParams(Protocol):
    user_uuid: str


class UserDeleteRepository(BaseRepository):
    def delete(self, params: UserDeleteRepositoryParams) -> None:
        getting_repository: IFindRepository[
            UserFindRepositoryParams, User
        ] = UserFindRepository(self.session)

        user: User = getting_repository.find_one(params)

        self.session.delete(user)
