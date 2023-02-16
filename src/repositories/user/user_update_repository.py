from dataclasses import dataclass
from datetime import date

from patterns.repository import IFindRepository, BaseRepository
from models import Usuario
from .user_getting_repository import UserGettingRepository, UserGettingRepositoryParam


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
        getting_repository_param: UserGettingRepositoryParam = (
            UserGettingRepositoryParam(uuid_user=param.uuid_user)
        )

        getting_repository: IFindRepository[
            UserGettingRepositoryParam, Usuario
        ] = UserGettingRepository(self.session)

        user: Usuario = getting_repository.get(getting_repository_param)

        user.cpf = param.document
        user.data_nascimento = param.birthday
        user.email = param.email
        user.nome = param.name
        user.senha = param.password
        user.ativo = param.status

        self.session.add(user)
