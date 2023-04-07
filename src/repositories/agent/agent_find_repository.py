from typing import Protocol, Optional

from patterns.repository import BaseRepository
from models import Departament, Agent
from exceptions import UserNotFoundError


class AgentFindRepositoryParams(Protocol):
    agent_uuid: str
    departament: Departament


class AgentFindRepository(BaseRepository):
    def find_one(self, params: AgentFindRepositoryParams) -> Agent:
        departament_user: Optional[Agent] = (
            self.session.query(Agent)
            .join(Departament, Agent.id_departamento == Departament.id)
            .filter(
                Departament.id == params.departament.id,
                Agent.id_uuid == params.agent_uuid,
            )
            .first()
        )

        if not departament_user:
            raise UserNotFoundError()

        return departament_user
