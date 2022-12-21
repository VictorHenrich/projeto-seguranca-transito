from dataclasses import dataclass
from datetime import date

from patterns.repository import IGettingRepository, BaseRepository
from models import Usuario
from repositories.user import (
    UserGettingRepository,
    UserGettingRepositoryParam
)


@dataclass
class UserUpdateRepositoryParam:
    uuid_user: str
    name: str
    email: str
    password: str
    document: str
    birthday: date
    status: bool


class UserUpdateRepository(BaseRepository):
    def update(self, param: UserUpdateRepositoryParam) -> None:
        with self.database.create_session() as session:
            getting_repository_param: UserGettingRepositoryParam = \
                UserGettingRepositoryParam(
                    uuid_user=param.uuid_user
                )

            getting_repository: IGettingRepository[UserGettingRepositoryParam, Usuario] = \
                UserGettingRepository(self.database)

            user: Usuario = getting_repository.get(getting_repository_param)

            user.cpf = param.document
            user.data_nascimento = param.birthday
            user.email = param.email
            user.nome = param.name
            user.senha = param.password
            user.ativo = param.status

            session.add(user)
            session.commit()