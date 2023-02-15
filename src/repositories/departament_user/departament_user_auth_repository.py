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
    def auth(self, param: DepartamentUserAuthRepositoryParam) -> UsuarioDepartamento:
        departament_user: UsuarioDepartamento = (
            self.session.query(UsuarioDepartamento)
            .join(Departamento, UsuarioDepartamento.id_departamento == Departamento.id)
            .filter(
                UsuarioDepartamento.acesso == param.user,
                UsuarioDepartamento.senha == param.password,
                Departamento.acesso == param.departament_access,
            )
            .first()
        )

        if not departament_user:
            raise UserNotFoundError()

        return departament_user
