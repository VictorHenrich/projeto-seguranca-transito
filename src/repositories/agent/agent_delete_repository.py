from typing import Protocol

from patterns.repository import BaseRepository, IFindRepository
from models import Agent, Departament
from .agent_find_repository import (
    AgentFindRepository,
    AgentFindRepositoryParams,
)


class AgentDeleteRepositoryParams(Protocol):
    departament: Departament
    agent_uuid: str


class AgentDeleteRepository(BaseRepository):
    def delete(self, params: AgentDeleteRepositoryParams) -> None:
        getting_repository: IFindRepository[
            AgentFindRepositoryParams, Agent
        ] = AgentFindRepository(self.session)

        user_departament: Agent = getting_repository.find_one(params)

        self.session.delete(user_departament)
