from typing import Protocol

from patterns.repository import BaseRepository
from models import Agent, Departament


class AgentUpdateRepositoryParam(Protocol):
    departament_user: Agent
    departament: Departament
    name: str
    access: str
    password: str
    position: str


class AgentUpdateRepository(BaseRepository):
    def update(self, params: AgentUpdateRepositoryParam) -> None:
        params.departament_user.nome = params.name
        params.departament_user.acesso = params.access
        params.departament_user.senha = params.password
        params.departament_user.cargo = params.position

        self.session.add(params.departament_user)
