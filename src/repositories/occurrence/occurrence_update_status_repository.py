from typing import Protocol, Literal, TypeAlias

from .occurrence_find_repository import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)
from patterns.repository import BaseRepository, IFindRepository
from models import Occurrence


OccurrenceStatus: TypeAlias = Literal["ANDAMENTO", "PROCESSO", "FALHA", "SUCESSO"]


class OccurrenceUpdateStatusRepositoryParams(Protocol):
    occurrence_uuid: str
    status: OccurrenceStatus


class OccurrenceUpdateStatusRepository(BaseRepository):
    def update(self, params: OccurrenceUpdateStatusRepositoryParams) -> None:
        occurrence_find_service: IFindRepository[
            OccurrenceFindRepositoryParams, Occurrence
        ] = OccurrenceFindRepository(self.session)

        occurrence: Occurrence = occurrence_find_service.find_one(params)

        occurrence.status = params.status

        self.session.add(occurrence)
