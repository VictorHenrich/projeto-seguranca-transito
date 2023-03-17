from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindRepository
from models import UsuarioDepartamento, Departamento
from .agent_find_repository import (
    AgentFindRepository,
    AgentFindRepositoryParams,
)


@dataclass
class AgentUpdateRepositoryParam:
    uuid_departament_user: str
    departament: Departamento
    name: str
    access: str
    password: str
    position: str


@dataclass
class AgentFindProps:
    uuid_departament_user: str
    departament: Departamento


class AgentUpdateRepository(BaseRepository):
    def update(self, params: AgentUpdateRepositoryParam) -> None:
        getting_repository: IFindRepository[
            AgentFindRepositoryParams, UsuarioDepartamento
        ] = AgentFindRepository(self.session)

        getting_repository_param: AgentFindRepositoryParams = (
            AgentFindProps(
                uuid_departament_user=params.uuid_departament_user,
                departament=params.departament,
            )
        )

        user_departament: UsuarioDepartamento = getting_repository.get(
            getting_repository_param
        )

        user_departament.nome = params.name
        user_departament.acesso = params.access
        user_departament.senha = params.password
        user_departament.cargo = params.position

        self.session.add(user_departament)
