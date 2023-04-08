from dataclasses import dataclass

from server import App
from patterns.repository import ICreateRepository
from models import Departament
from repositories.agent import (
    AgentCreateRepository,
    AgentCreateRepositoryParams,
)


@dataclass
class AgentCreationServiceProps:
    departament: Departament
    name: str
    access: str
    password: str
    position: str


class AgentCreationService:
    def execute(self, props: AgentCreationServiceProps) -> None:
        with App.databases.create_session() as session:
            creating_repository: ICreateRepository[
                AgentCreateRepositoryParams, None
            ] = AgentCreateRepository(session)

            creating_repository.create(props)

            session.commit()
