from typing import Optional, Protocol

from patterns.repository import BaseRepository
from models import User
from exceptions import UserNotFoundError


class UserFindRepositoryParams(Protocol):
    user_uuid: str


class UserFindRepository(BaseRepository):
    def find_one(self, params: UserFindRepositoryParams) -> User:
        user: Optional[User] = (
            self.session.query(User).filter(User.id_uuid == params.user_uuid).first()
        )

        if not user:
            raise UserNotFoundError()

        return user
