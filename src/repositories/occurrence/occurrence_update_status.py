from typing import Protocol

from patterns.repository import BaseRepository
from models import Occurrence
from utils.types import OccurrenceStatus


class OccurrenceUpdateStatusRepositoryParams(Protocol):
    occurrence: Occurrence
    status: OccurrenceStatus


class OccurrenceUpdateStatusRepository(BaseRepository):
    def update(self, params: OccurrenceUpdateStatusRepositoryParams) -> None:
        occurrence: Occurrence = params.occurrence

        occurrence.status = params.status.value

        self.session.add(occurrence)
