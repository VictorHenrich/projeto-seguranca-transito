from dataclasses import dataclass

from start import app
from patterns.repository import IFindRepository
from repositories.agent import (
    AgentFindRepository,
    AgentFindRepositoryParams,
)
from models import UsuarioDepartamento, Departamento


@dataclass
class AgentFindProps:
    uuid_departament_user: str
    departament: Departamento


class AgentGettingService:
    def execute(
        self, departament: Departamento, uuid_departament_user: UsuarioDepartamento
    ) -> UsuarioDepartamento:
        with app.databases.create_session() as session:
            getting_repository_param: AgentFindRepositoryParams = (
                AgentFindProps(
                    departament=departament, uuid_departament_user=uuid_departament_user
                )
            )

            getting_repository: IFindRepository[
                AgentFindRepositoryParams, UsuarioDepartamento
            ] = AgentFindRepository(session)

            user: UsuarioDepartamento = getting_repository.get(getting_repository_param)

            return user
