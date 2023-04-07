from typing import Protocol, Optional
from patterns.repository import BaseRepository
from models import Departament, Agent
from exceptions import UserNotFoundError


class AgentAuthRepositoryParams(Protocol):
    user: str
    password: str
    departament_access: str


class AgentAuthRepository(BaseRepository):
    def auth(self, params: AgentAuthRepositoryParams) -> Agent:
        departament_user: Optional[Agent] = (
            self.session.query(Agent)
            .join(Departament, Agent.id_departamento == Departament.id)
            .filter(
                Agent.acesso == params.user,
                Agent.senha == params.password,
                Departament.acesso == params.departament_access,
            )
            .first()
        )

        if not departament_user:
            raise UserNotFoundError()

        return departament_user
