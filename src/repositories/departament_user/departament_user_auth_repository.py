from dataclasses import dataclass
from patterns.repository import BaseRepository
from models import Departamento, UsuarioDepartamento
from exceptions import UserNotFoundError


@dataclass
class DepartamentUserAuthRepositoryParam:
    user: str
    password: str
    departament_access: str


class DepartamentUserAuthRepository(BaseRepository):
    def auth(self, params: DepartamentUserAuthRepositoryParam) -> UsuarioDepartamento:
        departament_user: UsuarioDepartamento = (
            self.session.query(UsuarioDepartamento)
            .join(Departamento, UsuarioDepartamento.id_departamento == Departamento.id)
            .filter(
                UsuarioDepartamento.acesso == params.user,
                UsuarioDepartamento.senha == params.password,
                Departamento.acesso == params.departament_access,
            )
            .first()
        )

        if not departament_user:
            raise UserNotFoundError()

        return departament_user
