from typing import Protocol
from datetime import date

from patterns.repository import IFindRepository, BaseRepository
from models import User
from .user_find_repository import UserFindRepository, UserFindRepositoryParams


class UserUpdateRepositoryParams(Protocol):
    user_uuid: str
    name: str
    email: str
    password: str
    document: str
    birthday: date
    status: bool


class UserUpdateRepository(BaseRepository):
    def update(self, params: UserUpdateRepositoryParams) -> None:
        getting_repository: IFindRepository[
            UserFindRepositoryParams, User
        ] = UserFindRepository(self.session)

        user: User = getting_repository.find_one(params)

        user.cpf = params.document
        user.data_nascimento = params.birthday
        user.email = params.email
        user.nome = params.name
        user.senha = params.password
        user.ativo = params.status

        self.session.add(user)
