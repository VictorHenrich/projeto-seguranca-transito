from typing import Protocol, Optional

from patterns.repository import BaseRepository
from models import Departament
from exceptions import DepartamentNotFoundError


class DepartamentFindRepositoryParams(Protocol):
    departament_id: int


class DepartamentFindRepository(BaseRepository):
    def find_one(self, params: DepartamentFindRepositoryParams) -> Departament:
        departament: Optional[Departament] = (
            self.session.query(Departament)
            .filter(Departament.id == params.departament_id)
            .first()
        )

        if not departament:
            raise DepartamentNotFoundError()

        return departament
