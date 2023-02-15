from dataclasses import dataclass

from patterns.repository import BaseRepository
from models import Departamento, UsuarioDepartamento
from exceptions import UserNotFoundError


@dataclass
class DepartamentUserGettingRepositoryParam:
    uuid_departament_user: str
    departament: Departamento


class DepartamentUserGettingRepository(BaseRepository):
    def get(self, param: DepartamentUserGettingRepositoryParam) -> UsuarioDepartamento:
        departament_user: UsuarioDepartamento = (
            self.session.query(UsuarioDepartamento)
            .join(Departamento, UsuarioDepartamento.id_departamento == Departamento.id)
            .filter(
                Departamento.id == param.departament.id,
                UsuarioDepartamento.id_uuid == param.uuid_departament_user,
            )
            .first()
        )

        if not departament_user:
            raise UserNotFoundError()

        return departament_user
