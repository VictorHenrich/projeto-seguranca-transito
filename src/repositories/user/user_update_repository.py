from typing import Optional
from dataclasses import dataclass
from datetime import date

from patterns.repository import IUpdateRepository, BaseRepository
from models import Usuario
from exceptions import UserNotFoundError


@dataclass
class UserUpdateRepositoryParam:
    uuid_user: str
    name: str
    email: str
    password: str
    document: str
    birthday: date
    status: bool


class UserUpdateRepository(BaseRepository, IUpdateRepository[UserUpdateRepositoryParam]):
    def update(self, param: UserUpdateRepositoryParam) -> None:
        with self.database.create_session() as session:
            user: Optional[Usuario] = \
                session\
                    .query(Usuario)\
                    .filter(Usuario.id_uuid == param.uuid_user)\
                    .first()

            if not user:
                raise UserNotFoundError()

            user.cpf = param.document
            user.data_nascimento = param.birthday
            user.email = param.email
            user.nome = param.name
            user.senha = param.password
            user.ativo = param.status

            session.add(user)
            session.commit()