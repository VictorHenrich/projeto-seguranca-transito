from dataclasses import dataclass

from patterns.repository import BaseRepository, IGettingRepository
from models import Ocorrencia
from .occurrence_getting_repository import (
    OccurrenceGettingRepository,
    OccurrenceGettingRepositoryParam
)



@dataclass
class OccurrenceExclusionRepositoryParam:
    uuid_occurrence: str



class OccurrenceExclusionRepository(BaseRepository):
    def delete(self, param: OccurrenceExclusionRepositoryParam) -> None:
        getting_repository_param: OccurrenceGettingRepositoryParam = \
            OccurrenceGettingRepositoryParam(
                uuid_occurrence=param.uuid_occurrence
            )

        getting_repository: IGettingRepository[OccurrenceGettingRepositoryParam, Ocorrencia] =\
            OccurrenceGettingRepository(self.session)

        occurrence: Ocorrencia = getting_repository.get(getting_repository_param)

        self.session.delete(occurrence)