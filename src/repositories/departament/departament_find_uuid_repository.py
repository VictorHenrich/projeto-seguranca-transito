from typing import Protocol

from patterns.repository import BaseRepository
from models import Departament
from exceptions import DepartamentNotFoundError


class DepartamentFindUUIDRepositoryParams(Protocol):
    uuid_departament: str


class DepartamentFindUUIDRepository(BaseRepository):
    def get(self, params: DepartamentFindUUIDRepositoryParams) -> Departament:
        departament: Departament = (
            self.session.query(Departament)
            .filter(Departament.id_uuid == params.uuid_departament)
            .first()
        )

        if not departament:
            raise DepartamentNotFoundError()

        return departament
