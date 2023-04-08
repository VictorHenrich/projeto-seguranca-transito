from dataclasses import dataclass

from server import App
from patterns.repository import IUpdateRepository
from repositories.agent import (
    AgentUpdateRepository,
    AgentUpdateRepositoryParams,
)
from models import Departament


@dataclass
class AgentUpdateServiceProps:
    agent_uuid: str
    departament: Departament
    name: str
    access: str
    password: str
    position: str


class AgentUpdateService:
    def execute(self, props: AgentUpdateServiceProps) -> None:
        with App.databases.create_session() as session:
            update_repository: IUpdateRepository[
                AgentUpdateRepositoryParams, None
            ] = AgentUpdateRepository(session)

            update_repository.update(props)

            session.commit()
