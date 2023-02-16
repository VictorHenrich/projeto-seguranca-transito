from typing import Protocol

from patterns.repository import BaseRepository
from models import Departamento
from exceptions import DepartamentNotFoundError


class DepartamentFindUUIDRepositoryParams(Protocol):
    uuid_departament: str


class DepartamentFindUUIDRepository(BaseRepository):
    def get(self, params: DepartamentFindUUIDRepositoryParams) -> Departamento:
        departament: Departamento = (
            self.session.query(Departamento)
            .filter(Departamento.id_uuid == params.uuid_departament)
            .first()
        )

        if not departament:
            raise DepartamentNotFoundError()

        return departament
