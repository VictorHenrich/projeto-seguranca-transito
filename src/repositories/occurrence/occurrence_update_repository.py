from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindRepository
from models import Ocorrencia
from .occurrence_find_repository import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


@dataclass
class OccurrenceUpdateRepositoryParam:
    uuid_occurrence: str
    description: str
    obs: str


@dataclass
class OccurrenceFindProps:
    uuid_occurrence: str


class OccurrenceUpdateRepository(BaseRepository):
    def update(self, params: OccurrenceUpdateRepositoryParam) -> None:
        getting_repository: IFindRepository[
            OccurrenceFindRepositoryParams, Ocorrencia
        ] = OccurrenceFindRepository(self.session)

        getting_repository_param: OccurrenceFindRepositoryParams = OccurrenceFindProps(
            uuid_occurrence=params.uuid_occurrence
        )

        occurrence: Ocorrencia = getting_repository.get(getting_repository_param)

        occurrence.descricao = params.description
        occurrence.obs = params.obs

        self.session.add(occurrence)
