from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindRepository
from models import Agent, Departament
from .agent_find_repository import (
    AgentFindRepository,
    AgentFindRepositoryParams,
)


@dataclass
class AgentUpdateRepositoryParam:
    uuid_departament_user: str
    departament: Departament
    name: str
    access: str
    password: str
    position: str


@dataclass
class AgentFindProps:
    uuid_departament_user: str
    departament: Departament


class AgentUpdateRepository(BaseRepository):
    def update(self, params: AgentUpdateRepositoryParam) -> None:
        getting_repository: IFindRepository[
            AgentFindRepositoryParams, Agent
        ] = AgentFindRepository(self.session)

        getting_repository_param: AgentFindRepositoryParams = AgentFindProps(
            uuid_departament_user=params.uuid_departament_user,
            departament=params.departament,
        )

        user_departament: Agent = getting_repository.get(getting_repository_param)

        user_departament.nome = params.name
        user_departament.acesso = params.access
        user_departament.senha = params.password
        user_departament.cargo = params.position

        self.session.add(user_departament)
