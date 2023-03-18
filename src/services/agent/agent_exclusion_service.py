from dataclasses import dataclass

from start import app
from patterns.repository import IDeleteRepository
from repositories.agent import (
    AgentDeleteRepository,
    AgentDeleteRepositoryParams,
)
from models import Agent, Departament


@dataclass
class AgentDeleteProps:
    epartament: str
    uuid_departament_user: str


class AgentExclusionService:
    def execute(self, departament: Departament, uuid_departament_user: Agent) -> None:
        with app.databases.create_session() as session:
            exclusion_repository_param: AgentDeleteRepositoryParams = AgentDeleteProps(
                departament=departament, uuid_departament_user=uuid_departament_user
            )

            exclusion_repository: IDeleteRepository[
                AgentDeleteRepositoryParams
            ] = AgentDeleteRepository(session)

            exclusion_repository.delete(exclusion_repository_param)

            session.commit()
