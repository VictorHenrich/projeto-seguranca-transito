from typing import Optional
from dataclasses import dataclass
from datetime import date

from patterns.repository import ICreationRepository, BaseRepository
from models import Usuario


@dataclass
class UserCreationRepositoryParam:
    name: str
    email: str
    password: str
    document: str
    birthday: Optional[date]


class UserCreationRepository(BaseRepository):
    def create(self, param: UserCreationRepositoryParam) -> None:
        user: Usuario = Usuario()

        user.cpf = param.document
        user.data_nascimento = param.birthday
        user.email = param.email
        user.nome = param.name
        user.senha = param.password
        user.ativo = True

        self.session.add(user)
