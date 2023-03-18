from typing import List
from dataclasses import dataclass

from start import app
from patterns.repository import IFindManyRepository
from repositories.agent import (
    AgentFindManyRepository,
    AgentFindManyRepositoryParams,
)
from models import Agent, Departament


@dataclass
class AgentListingServiceProps:
    departament: Departament


class AgentListingService:
    def execute(self, props: AgentListingServiceProps) -> List[Agent]:

        with app.databases.create_session() as session:
            listing_repository: IFindManyRepository[
                AgentFindManyRepositoryParams, Agent
            ] = AgentFindManyRepository(session)

            users: List[Agent] = listing_repository.list(props)

            return users
