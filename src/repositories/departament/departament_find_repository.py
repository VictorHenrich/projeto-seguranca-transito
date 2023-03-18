from typing import Protocol

from patterns.repository import BaseRepository
from models import Departament
from exceptions import DepartamentNotFoundError


class DepartamentFindRepositoryParams(Protocol):
    departament_id: int


class DepartamentFindRepository(BaseRepository):
    def get(self, params: DepartamentFindRepositoryParams) -> Departament:
        departament: Departament = (
            self.session.query(Departament)
            .filter(Departament.id == params.departament_id)
            .first()
        )

        if not departament:
            raise DepartamentNotFoundError()

        return departament
