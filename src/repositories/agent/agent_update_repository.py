from typing import Protocol

from patterns.repository import BaseRepository, IFindRepository
from .agent_find_repository import AgentFindRepository, AgentFindRepositoryParams
from models import Agent, Departament


class AgentUpdateRepositoryParams(Protocol):
    agent_uuid: str
    departament: Departament
    name: str
    access: str
    password: str
    position: str


class AgentUpdateRepository(BaseRepository):
    def update(self, params: AgentUpdateRepositoryParams) -> None:
        agent_find_repository: IFindRepository[
            AgentFindRepositoryParams, Agent
        ] = AgentFindRepository(self.session)

        agent: Agent = agent_find_repository.find_one(params)

        agent.nome = params.name
        agent.acesso = params.access
        agent.senha = params.password
        agent.cargo = params.position

        self.session.add(agent)
