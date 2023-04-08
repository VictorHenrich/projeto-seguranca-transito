from typing import List
from dataclasses import dataclass

from server import App
from patterns.repository import IFindManyRepository
from repositories.agent import (
    AgentFindManyRepository,
    AgentFindManyRepositoryParams,
)
from models import Agent, Departament


@dataclass
class AgentsFetchingServiceProps:
    departament: Departament


class AgentsFetchingService:
    def execute(self, props: AgentsFetchingServiceProps) -> List[Agent]:
        with App.databases.create_session() as session:
            listing_repository: IFindManyRepository[
                AgentFindManyRepositoryParams, Agent
            ] = AgentFindManyRepository(session)

            users: List[Agent] = listing_repository.find_many(props)

            return users
