from typing import List, Protocol

from patterns.repository import BaseRepository
from models import Departament, Agent


class AgentFindManyRepositoryParams(Protocol):
    departament: Departament


class AgentFindManyRepository(BaseRepository):
    def find_many(self, params: AgentFindManyRepositoryParams) -> List[Agent]:
        departament_users: List[Agent] = (
            self.session.query(Agent)
            .join(Departament, Agent.id_departamento == Departament.id)
            .filter(Agent.id_departamento == params.departament.id)
            .all()
        )

        return departament_users
