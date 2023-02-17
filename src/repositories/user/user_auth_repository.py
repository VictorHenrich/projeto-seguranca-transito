from dataclasses import dataclass

from patterns.repository import BaseRepository, IAuthRepository
from models import Usuario
from exceptions import UserNotFoundError


@dataclass
class UserAuthRepositoryParam:
    email: str
    password: str


class UserAuthRepository(BaseRepository):
    def auth(self, params: UserAuthRepositoryParam) -> Usuario:
        user: Usuario = (
            self.session.query(Usuario)
            .filter(
                Usuario.email == params.email.upper(), Usuario.senha == params.password
            )
            .first()
        )

        if not user:
            raise UserNotFoundError()

        return user
