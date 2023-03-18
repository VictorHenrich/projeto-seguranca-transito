from typing import Optional, Protocol
from datetime import date

from patterns.repository import BaseRepository
from models import User


class UserCreateRepositoryParams(Protocol):
    name: str
    email: str
    password: str
    document: str
    birthday: Optional[date]


class UserCreateRepository(BaseRepository):
    def create(self, params: UserCreateRepositoryParams) -> None:
        user: User = User()

        user.cpf = params.document
        user.data_nascimento = params.birthday
        user.email = params.email
        user.nome = params.name
        user.senha = params.password
        user.ativo = True

        self.session.add(user)
