from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from repositories.agent import (
    AgentFindRepository,
    AgentFindRepositoryParams,
)
from models import Agent, Departament


@dataclass
class AgentGettingServiceProps:
    agent_uuid: str
    departament: Departament


class AgentGettingService:
    def execute(self, props: AgentGettingServiceProps) -> Agent:
        with App.databases.create_session() as session:
            getting_repository: IFindRepository[
                AgentFindRepositoryParams, Agent
            ] = AgentFindRepository(session)

            user: Agent = getting_repository.find_one(props)

            return user
