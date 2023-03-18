from typing import Protocol

from patterns.repository import BaseRepository
from models import Occurrence, User, Departament


class OccurrenceCreateRepositoryParam(Protocol):
    user: User
    departament: Departament
    description: str
    obs: str


class OccurrenceCreateRepository(BaseRepository):
    def create(self, params: OccurrenceCreateRepositoryParam) -> None:
        occurrence: Occurrence = Occurrence()

        occurrence.id_departamento = params.departament.id
        occurrence.id_usuario = params.user.id
        occurrence.descricao = params.description
        occurrence.obs = params.obs
        occurrence.status = "ANDAMENTO"

        self.session.add(occurrence)
