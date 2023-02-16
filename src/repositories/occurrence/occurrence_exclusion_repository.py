from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindRepository
from models import Ocorrencia
from .occurrence_find_repository import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


@dataclass
class OccurrenceExclusionRepositoryParam:
    uuid_occurrence: str


class OccurrenceExclusionRepository(BaseRepository):
    def delete(self, param: OccurrenceExclusionRepositoryParam) -> None:
        getting_repository: IFindRepository[
            OccurrenceFindRepositoryParams, Ocorrencia
        ] = OccurrenceFindRepository(self.session)

        occurrence: Ocorrencia = getting_repository.get(param)

        self.session.delete(occurrence)
