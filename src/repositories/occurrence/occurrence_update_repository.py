from dataclasses import dataclass

from patterns.repository import BaseRepository, IGettingRepository
from models import Ocorrencia
from .occurrence_getting_repository import (
    OccurrenceGettingRepository,
    OccurrenceGettingRepositoryParam,
)


@dataclass
class OccurrenceUpdateRepositoryParam:
    uuid_occurrence: str
    description: str
    obs: str


class OccurrenceUpdateRepository(BaseRepository):
    def update(self, param: OccurrenceUpdateRepositoryParam) -> None:
        getting_repository: IGettingRepository[
            OccurrenceGettingRepositoryParam, Ocorrencia
        ] = OccurrenceGettingRepository(self.session)

        getting_repository_param: OccurrenceGettingRepositoryParam = (
            OccurrenceGettingRepositoryParam(uuid_occurrence=param.uuid_occurrence)
        )

        occurrence: Ocorrencia = getting_repository.get(getting_repository_param)

        occurrence.descricao = param.description
        occurrence.obs = param.obs

        self.session.add(occurrence)
