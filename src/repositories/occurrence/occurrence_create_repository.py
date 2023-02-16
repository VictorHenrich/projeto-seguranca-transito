from typing import Protocol

from patterns.repository import BaseRepository
from models import Ocorrencia, Usuario, Departamento


class OccurrenceCreateRepositoryParam(Protocol):
    user: Usuario
    departament: Departamento
    description: str
    obs: str


class OccurrenceCreateRepository(BaseRepository):
    def create(self, params: OccurrenceCreateRepositoryParam) -> None:
        occurrence: Ocorrencia = Ocorrencia()

        occurrence.id_departamento = params.departament.id
        occurrence.id_usuario = params.user.id
        occurrence.descricao = params.description
        occurrence.obs = params.obs
        occurrence.status = "ANDAMENTO"

        self.session.add(occurrence)
