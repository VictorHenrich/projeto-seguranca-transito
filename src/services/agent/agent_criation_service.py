from dataclasses import dataclass

from start import app
from patterns.repository import ICreateRepository
from models import Departamento
from repositories.agent import (
    AgentCreateRepository,
    AgentCreateRepositoryParam,
)


@dataclass
class AgentCreateProps:
    departament: Departamento
    name: str
    access: str
    password: str
    position: str


class AgentCriationService:
    def execute(
        self,
        departament: Departamento,
        name: str,
        user: str,
        password: str,
        position: str,
    ) -> None:
        with app.databases.create_session() as session:
            creating_repository_param: AgentCreateRepositoryParam = (
                AgentCreateProps(
                    departament=departament,
                    name=name,
                    access=user,
                    password=password,
                    position=position,
                )
            )

            creating_repository: ICreateRepository[
                AgentCreateRepositoryParam
            ] = AgentCreateRepository(session)

            creating_repository.create(creating_repository_param)

            session.commit()
