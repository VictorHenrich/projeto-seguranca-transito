from dataclasses import dataclass
from patterns.repository import BaseRepository
from models import Departamento, UsuarioDepartamento


@dataclass
class DepartamentUserCreationRepositoryParam:
    departament: Departamento
    name: str
    access: str
    password: str
    position: str


class DepartamentUserCreationRepository(BaseRepository):
    def create(self, param: DepartamentUserCreationRepositoryParam) -> None:
        departament_user: UsuarioDepartamento = UsuarioDepartamento()

        departament_user.id_departamento = param.departament.id
        departament_user.nome = param.name
        departament_user.acesso = param.access
        departament_user.senha = param.password
        departament_user.cargo = param.position

        self.session.add(departament_user)
