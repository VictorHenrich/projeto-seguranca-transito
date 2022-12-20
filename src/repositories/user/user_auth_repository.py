from dataclasses import dataclass

from patterns.repository import BaseRepository, IAuthRepository
from models import Usuario
from exceptions import UserNotFoundError


@dataclass
class UserAuthRepositoryParam:
    email: str
    password: str


class UserAuthRepository(BaseRepository, IAuthRepository[UserAuthRepositoryParam, Usuario]):
    def auth(self, param: UserAuthRepositoryParam) -> Usuario:
        with self.database.create_session() as session:
            user: Usuario = \
                session\
                    .query(Usuario)\
                    .filter(
                        Usuario.nome == param.email.upper(),
                        Usuario.senha == param.password.upper()
                    )\
                    .first()

            if not user:
                raise UserNotFoundError()

            return user