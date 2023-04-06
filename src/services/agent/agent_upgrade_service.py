from dataclasses import dataclass

from server import App
from patterns.repository import IUpdateRepository
from repositories.agent import (
    AgentUpdateRepository,
    AgentUpdateRepositoryParam,
)
from models import Agent, Departament


@dataclass
class AgentUpgradeServiceProps:
    departament_user: Agent
    departament: Departament
    name: str
    access: str
    password: str
    position: str


class AgentUpgradeService:
    def execute(self, props: AgentUpgradeServiceProps) -> None:
        with App.databases.create_session() as session:
            update_repository: IUpdateRepository[
                AgentUpdateRepositoryParam, None
            ] = AgentUpdateRepository(session)

            update_repository.update(props)

            session.commit()
