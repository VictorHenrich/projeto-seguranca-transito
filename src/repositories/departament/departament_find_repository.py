from typing import Protocol

from patterns.repository import BaseRepository
from models import Departamento
from exceptions import DepartamentNotFoundError


class DepartamentFindRepositoryParams(Protocol):
    departament_id: str


class DepartamentFindRepository(BaseRepository):
    def get(self, params: DepartamentFindRepositoryParams) -> Departamento:
        departament: Departamento = (
            self.session.query(Departamento)
            .filter(Departamento.id == params.departament_id)
            .first()
        )

        if not departament:
            raise DepartamentNotFoundError()

        return departament
