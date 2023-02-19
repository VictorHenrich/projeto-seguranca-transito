from typing import Protocol

from patterns.repository import BaseRepository
from models import Departamento, UsuarioDepartamento


class DepartamentUserCreateRepositoryParam(Protocol):
    departament: Departamento
    name: str
    access: str
    password: str
    position: str


class DepartamentUserCreateRepository(BaseRepository):
    def create(self, params: DepartamentUserCreateRepositoryParam) -> None:
        departament_user: UsuarioDepartamento = UsuarioDepartamento()

        departament_user.id_departamento = params.departament.id
        departament_user.nome = params.name
        departament_user.acesso = params.access
        departament_user.senha = params.password
        departament_user.cargo = params.position

        self.session.add(departament_user)
