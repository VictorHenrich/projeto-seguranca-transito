from typing import Protocol

from patterns.repository import BaseRepository
from models import Departament, Agent
from exceptions import UserNotFoundError


class AgentFindRepositoryParams(Protocol):
    uuid_departament_user: str
    departament: Departament


class AgentFindRepository(BaseRepository):
    def get(self, params: AgentFindRepositoryParams) -> Agent:
        departament_user: Agent = (
            self.session.query(Agent)
            .join(Departament, Agent.id_departamento == Departament.id)
            .filter(
                Departament.id == params.departament.id,
                Agent.id_uuid == params.uuid_departament_user,
            )
            .first()
        )

        if not departament_user:
            raise UserNotFoundError()

        return departament_user
