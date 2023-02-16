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
    def update(self, param: OccurrenceUpdateRepositoryParam) -> None:
        getting_repository: IFindRepository[
            OccurrenceFindRepositoryParams, Ocorrencia
        ] = OccurrenceFindRepository(self.session)

        getting_repository_param: OccurrenceFindRepositoryParams = OccurrenceFindProps(
            uuid_occurrence=param.uuid_occurrence
        )

        occurrence: Ocorrencia = getting_repository.get(getting_repository_param)

        occurrence.descricao = param.description
        occurrence.obs = param.obs

        self.session.add(occurrence)
