from dataclasses import dataclass
from typing import Optional

from patterns.repository import BaseRepository, IExclusionRepository
from models import Usuario
from exceptions import UserNotFoundError



@dataclass
class UserExclusionRepositoryParam:
    uuid_ser: str


class UserExclusionRepository(BaseRepository, IExclusionRepository[UserExclusionRepositoryParam]):
    def delete(self, param: UserExclusionRepositoryParam) -> None:
        with self.database.create_session() as session:
            user: Optional[Usuario] = \
                session\
                    .query(Usuario)\
                    .filter(Usuario.id_uuid == param.uuid_ser)\
                    .first()

            if not user:
                raise UserNotFoundError()

            session.delete(user)
            session.commit()
