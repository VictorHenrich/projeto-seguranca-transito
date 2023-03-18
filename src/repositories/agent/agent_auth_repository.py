from dataclasses import dataclass
from patterns.repository import BaseRepository
from models import Departament, Agent
from exceptions import UserNotFoundError


@dataclass
class AgentAuthRepositoryParam:
    user: str
    password: str
    departament_access: str


class AgentAuthRepository(BaseRepository):
    def auth(self, params: AgentAuthRepositoryParam) -> Agent:
        departament_user: Agent = (
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
