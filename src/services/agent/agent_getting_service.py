from dataclasses import dataclass

from start import app
from patterns.repository import IFindRepository
from repositories.agent import (
    AgentFindRepository,
    AgentFindRepositoryParams,
)
from models import Agent, Departament


@dataclass
class AgentFindProps:
    uuid_departament_user: str
    departament: Departament


class AgentGettingService:
    def execute(self, departament: Departament, uuid_departament_user: Agent) -> Agent:
        with app.databases.create_session() as session:
            getting_repository_param: AgentFindRepositoryParams = AgentFindProps(
                departament=departament, uuid_departament_user=uuid_departament_user
            )

            getting_repository: IFindRepository[
                AgentFindRepositoryParams, Agent
            ] = AgentFindRepository(session)

            user: Agent = getting_repository.get(getting_repository_param)

            return user
