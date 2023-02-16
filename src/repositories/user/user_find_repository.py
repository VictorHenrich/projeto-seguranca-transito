from typing import Optional, Protocol

from patterns.repository import BaseRepository
from models import Usuario
from exceptions import UserNotFoundError



class UserFindRepositoryParams(Protocol):
    uuid_user: str


class UserFindRepository(BaseRepository):
    def get(self, params: UserFindRepositoryParams) -> Usuario:
        user: Optional[Usuario] = (
            self.session.query(Usuario)
            .filter(Usuario.id_uuid == params.uuid_user)
            .first()
        )

        if not user:
            raise UserNotFoundError()

        return user
