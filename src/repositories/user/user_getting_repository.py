from dataclasses import dataclass
from typing import Optional

from patterns.repository import BaseRepository, IGettingRepository
from models import Usuario
from exceptions import UserNotFoundError


@dataclass
class UserGettingRepositoryParam:
    uuid_user: str


class UserGettingRepository(BaseRepository, IGettingRepository[UserGettingRepositoryParam, Usuario]):
    def get(self, param: UserGettingRepositoryParam) -> Usuario:
        with self.database.create_session() as session:
            user: Optional[Usuario] = \
                session\
                    .query(Usuario)\
                    .filter(Usuario.id_uuid == param.uuid_user)\
                    .filter()

            if not user:
                raise UserNotFoundError()

            return user

