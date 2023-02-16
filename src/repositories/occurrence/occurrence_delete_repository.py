from typing import Protocol

from patterns.repository import BaseRepository, IFindRepository
from models import Ocorrencia
from .occurrence_find_repository import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)



class OccurrenceDeleteRepositoryParams(Protocol):
    uuid_occurrence: str


class OccurrenceDeleteRepository(BaseRepository):
    def delete(self, params: OccurrenceDeleteRepositoryParams) -> None:
        getting_repository: IFindRepository[
            OccurrenceFindRepositoryParams, Ocorrencia
        ] = OccurrenceFindRepository(self.session)

        occurrence: Ocorrencia = getting_repository.get(params)

        self.session.delete(occurrence)
