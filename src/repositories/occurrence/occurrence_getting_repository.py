from dataclasses import dataclass

from patterns.repository import BaseRepository
from models import Ocorrencia
from exceptions import OccurrenceNotFoundError



@dataclass
class OccurrenceGettingRepositoryParam:
    uuid_occurrence: str


class OccurrenceGettingRepository(BaseRepository):
    def get(self, param: OccurrenceGettingRepositoryParam) -> Ocorrencia:
        occurrence: Ocorrencia = \
            self.session\
                    .query(Ocorrencia)\
                    .filter(Ocorrencia.id_uuid == param.uuid_occurrence)\
                    .first()

        if not occurrence:
            raise OccurrenceNotFoundError()

        return occurrence