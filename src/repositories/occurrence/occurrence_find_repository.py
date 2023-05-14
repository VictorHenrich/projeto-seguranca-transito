from typing import Protocol, Optional

from patterns.repository import BaseRepository
from models import Occurrence
from exceptions import OccurrenceNotFoundError


class OccurrenceFindRepositoryParams(Protocol):
    occurrence_uuid: str


class OccurrenceFindRepository(BaseRepository):
    def find_one(self, params: OccurrenceFindRepositoryParams) -> Occurrence:
        occurrence: Optional[Occurrence] = (
            self.session.query(Occurrence)
            .filter(Occurrence.id_uuid == params.occurrence_uuid)
            .first()
        )

        if not occurrence:
            raise OccurrenceNotFoundError()

        return occurrence
