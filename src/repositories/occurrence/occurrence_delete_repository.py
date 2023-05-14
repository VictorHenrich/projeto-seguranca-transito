from typing import Protocol

from patterns.repository import BaseRepository, IFindRepository
from models import Occurrence
from .occurrence_find_repository import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


class OccurrenceDeleteRepositoryParams(Protocol):
    occurrence_uuid: str


class OccurrenceDeleteRepository(BaseRepository):
    def delete(self, params: OccurrenceDeleteRepositoryParams) -> None:
        getting_repository: IFindRepository[
            OccurrenceFindRepositoryParams, Occurrence
        ] = OccurrenceFindRepository(self.session)

        occurrence: Occurrence = getting_repository.find_one(params)

        self.session.delete(occurrence)
