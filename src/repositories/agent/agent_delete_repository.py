from dataclasses import dataclass
from typing import Protocol

from patterns.repository import BaseRepository, IFindRepository
from models import UsuarioDepartamento, Departamento
from .agent_find_repository import (
    AgentFindRepository,
    AgentFindRepositoryParams,
)


class AgentDeleteRepositoryParams(Protocol):
    departament: Departamento
    uuid_departament_user: str


@dataclass
class AgentFindProps:
    uuid_departament_user: str
    departament: Departamento


class AgentDeleteRepository(BaseRepository):
    def delete(self, params: AgentDeleteRepositoryParams) -> None:
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

        self.session.delete(user_departament)
