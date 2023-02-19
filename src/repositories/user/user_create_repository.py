from typing import Optional
from dataclasses import dataclass
from datetime import date

from patterns.repository import BaseRepository
from models import Usuario


@dataclass
class UserCreateRepositoryParams:
    name: str
    email: str
    password: str
    document: str
    birthday: Optional[date]


class UserCreateRepository(BaseRepository):
    def create(self, params: UserCreateRepositoryParams) -> None:
        user: Usuario = Usuario()

        user.cpf = params.document
        user.data_nascimento = params.birthday
        user.email = params.email
        user.nome = params.name
        user.senha = params.password
        user.ativo = True

        self.session.add(user)
