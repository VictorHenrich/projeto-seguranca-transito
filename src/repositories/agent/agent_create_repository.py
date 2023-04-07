from typing import Protocol

from patterns.repository import BaseRepository
from models import Departament, Agent


class AgentCreateRepositoryParams(Protocol):
    departament: Departament
    name: str
    access: str
    password: str
    position: str


class AgentCreateRepository(BaseRepository):
    def create(self, params: AgentCreateRepositoryParams) -> None:
        departament_user: Agent = Agent()

        departament_user.id_departamento = params.departament.id
        departament_user.nome = params.name
        departament_user.acesso = params.access
        departament_user.senha = params.password
        departament_user.cargo = params.position

        self.session.add(departament_user)
