from typing import Protocol

from patterns.repository import BaseRepository
from models import Ocorrencia
from exceptions import OccurrenceNotFoundError


class OccurrenceFindRepositoryParams(Protocol):
    uuid_occurrence: str


class OccurrenceFindRepository(BaseRepository):
    def get(self, param: OccurrenceFindRepositoryParams) -> Ocorrencia:
        occurrence: Ocorrencia = (
            self.session.query(Ocorrencia)
            .filter(Ocorrencia.id_uuid == param.uuid_occurrence)
            .first()
        )

        if not occurrence:
            raise OccurrenceNotFoundError()

        return occurrence
