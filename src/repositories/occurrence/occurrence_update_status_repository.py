from typing import Protocol, Literal, TypeAlias

from patterns.repository import BaseRepository
from models import Occurrence


OccurrenceStatus: TypeAlias = Literal["ANDAMENTO", "PROCESSO", "FALHA", "SUCESSO"]


class OccurrenceUpdateStatusRepositoryParams(Protocol):
    occurrence: Occurrence
    status: OccurrenceStatus


class OccurrenceUpdateStatusRepository(BaseRepository):
    def update(self, params: OccurrenceUpdateStatusRepositoryParams) -> None:
        occurrence: Occurrence = params.occurrence

        occurrence.status = params.status

        self.session.add(occurrence)
