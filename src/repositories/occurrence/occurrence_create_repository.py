from typing import Protocol

from models import User, Occurrence
from patterns.repository import BaseRepository


class OccurrenceCreateRepositoryParam(Protocol):
    user: User
    code_external: str
    description: str
    obs: str


class OccurrenceCreateRepository(BaseRepository):
    def create(self, params: OccurrenceCreateRepositoryParam) -> None:
        occurrence: Occurrence = Occurrence()

        occurrence.id_usuario = params.user.id
        occurrence.codigo_externo = params.code_external
        occurrence.descricao = params.description
        occurrence.obs = params.obs
        occurrence.status = "ANDAMENTO"

        self.session.add(occurrence)
