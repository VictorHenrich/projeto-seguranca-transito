from typing import Optional, Protocol

from patterns.repository import BaseRepository
from models import User
from exceptions import UserNotFoundError


class UserFindRepositoryParams(Protocol):
    uuid_user: str


class UserFindRepository(BaseRepository):
    def get(self, params: UserFindRepositoryParams) -> User:
        user: Optional[User] = (
            self.session.query(User).filter(User.id_uuid == params.uuid_user).first()
        )

        if not user:
            raise UserNotFoundError()

        return user
