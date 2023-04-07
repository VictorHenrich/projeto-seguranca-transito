from dataclasses import dataclass
from typing import Protocol
from datetime import date

from patterns.repository import IFindRepository, BaseRepository
from models import User
from .user_find_repository import UserFindRepository, UserFindRepositoryParams


class UserUpdateRepositoryParams(Protocol):
    uuid_user: str
    name: str
    email: str
    password: str
    document: str
    birthday: date
    status: bool


@dataclass
class UserFindProps:
    uuid_user: str


class UserUpdateRepository(BaseRepository):
    def update(self, params: UserUpdateRepositoryParams) -> None:
        getting_repository_param: UserFindRepositoryParams = UserFindProps(
            uuid_user=params.uuid_user
        )

        getting_repository: IFindRepository[
            UserFindRepositoryParams, User
        ] = UserFindRepository(self.session)

        user: User = getting_repository.get(getting_repository_param)

        user.cpf = params.document
        user.data_nascimento = params.birthday
        user.email = params.email
        user.nome = params.name
        user.senha = params.password
        user.ativo = params.status

        self.session.add(user)
