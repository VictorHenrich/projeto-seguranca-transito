from typing import List, Protocol

from patterns.repository import BaseRepository
from models import Departamento, UsuarioDepartamento


class AgentFindManyRepositoryParams(Protocol):
    departament: Departamento


class AgentFindManyRepository(BaseRepository):
    def list(
        self, params: AgentFindManyRepositoryParams
    ) -> List[UsuarioDepartamento]:
        departament_users: List[UsuarioDepartamento] = (
            self.session.query(UsuarioDepartamento)
            .join(Departamento, UsuarioDepartamento.id_departamento == Departamento.id)
            .filter(UsuarioDepartamento.id_departamento == params.departament.id)
            .all()
        )

        return departament_users
