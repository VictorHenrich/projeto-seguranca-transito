from dataclasses import dataclass

from start import app
from patterns.repository import IFindRepository
from models import Occurrence
from repositories.occurrence import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


@dataclass
class OccurrenceFindProps:
    uuid_occurrence: str


class OccurrenceGettingService:
    def execute(self, uuid_occurrence: str) -> Occurrence:
        with app.databases.create_session() as session:
            getting_repository_param: OccurrenceFindRepositoryParams = (
                OccurrenceFindProps(uuid_occurrence=uuid_occurrence)
            )

            getting_repository: IFindRepository[
                OccurrenceFindRepositoryParams, Occurrence
            ] = OccurrenceFindRepository(session)

            occurrence: Occurrence = getting_repository.get(getting_repository_param)

            return occurrence
