from dataclasses import dataclass

from patterns.repository import BaseRepository, IAuthRepository
from models import User
from exceptions import UserNotFoundError


@dataclass
class UserAuthRepositoryParam:
    email: str
    password: str


class UserAuthRepository(BaseRepository):
    def auth(self, params: UserAuthRepositoryParam) -> User:
        user: User = (
            self.session.query(User)
            .filter(User.email == params.email.upper(), User.senha == params.password)
            .first()
        )

        if not user:
            raise UserNotFoundError()

        return user
