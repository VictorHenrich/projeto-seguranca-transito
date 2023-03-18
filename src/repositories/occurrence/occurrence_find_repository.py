from typing import Protocol

from patterns.repository import BaseRepository
from models import Occurrence
from exceptions import OccurrenceNotFoundError


class OccurrenceFindRepositoryParams(Protocol):
    uuid_occurrence: str


class OccurrenceFindRepository(BaseRepository):
    def get(self, param: OccurrenceFindRepositoryParams) -> Occurrence:
        occurrence: Occurrence = (
            self.session.query(Occurrence)
            .filter(Occurrence.id_uuid == param.uuid_occurrence)
            .first()
        )

        if not occurrence:
            raise OccurrenceNotFoundError()

        return occurrence
