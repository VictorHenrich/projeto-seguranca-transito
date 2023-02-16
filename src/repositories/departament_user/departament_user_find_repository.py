from typing import Protocol

from patterns.repository import BaseRepository
from models import Departamento, UsuarioDepartamento
from exceptions import UserNotFoundError


class DepartamentUserFindRepositoryParams(Protocol):
    uuid_departament_user: str
    departament: Departamento


class DepartamentUserFindRepository(BaseRepository):
    def get(self, params: DepartamentUserFindRepositoryParams) -> UsuarioDepartamento:
        departament_user: UsuarioDepartamento = (
            self.session.query(UsuarioDepartamento)
            .join(Departamento, UsuarioDepartamento.id_departamento == Departamento.id)
            .filter(
                Departamento.id == params.departament.id,
                UsuarioDepartamento.id_uuid == params.uuid_departament_user,
            )
            .first()
        )

        if not departament_user:
            raise UserNotFoundError()

        return departament_user
