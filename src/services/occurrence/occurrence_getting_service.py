from dataclasses import dataclass

from start import app
from patterns.repository import IFindRepository
from models import Occurrence
from repositories.occurrence import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


@dataclass
class OccurrenceGettingServiceProps:
    uuid_occurrence: str


class OccurrenceGettingService:
    def execute(self, props: OccurrenceGettingServiceProps) -> Occurrence:
        with app.databases.create_session() as session:
            getting_repository: IFindRepository[
                OccurrenceFindRepositoryParams, Occurrence
            ] = OccurrenceFindRepository(session)

            occurrence: Occurrence = getting_repository.get(props)

            return occurrence
