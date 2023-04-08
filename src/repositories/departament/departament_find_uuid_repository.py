from typing import Protocol, Optional

from patterns.repository import BaseRepository
from models import Departament
from exceptions import DepartamentNotFoundError


class DepartamentFindUUIDRepositoryParams(Protocol):
    departament_uuid: str


class DepartamentFindUUIDRepository(BaseRepository):
    def find_one(self, params: DepartamentFindUUIDRepositoryParams) -> Departament:
        departament: Optional[Departament] = (
            self.session.query(Departament)
            .filter(Departament.id_uuid == params.departament_uuid)
            .first()
        )

        if not departament:
            raise DepartamentNotFoundError()

        return departament
