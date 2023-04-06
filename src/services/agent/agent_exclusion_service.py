from dataclasses import dataclass

from server import App
from patterns.repository import IDeleteRepository
from repositories.agent import (
    AgentDeleteRepository,
    AgentDeleteRepositoryParams,
)
from models import Departament


@dataclass
class AgentExclusionServiceProps:
    departament: Departament
    uuid_departament_user: str


class AgentExclusionService:
    def execute(self, props: AgentExclusionServiceProps) -> None:
        with App.databases.create_session() as session:
            exclusion_repository: IDeleteRepository[
                AgentDeleteRepositoryParams, None
            ] = AgentDeleteRepository(session)

            exclusion_repository.delete(props)

            session.commit()
