from dataclasses import dataclass

from server import App
from patterns.repository import IFindRepository
from models import Occurrence
from repositories.occurrence import (
    OccurrenceFindRepository,
    OccurrenceFindRepositoryParams,
)


@dataclass
class OccurrenceFindProps:
    occurrence_uuid: str


class OccurrenceGettingService:
    def __init__(self, occurrence_uuid: str) -> None:
        self.__props: OccurrenceFindProps = OccurrenceFindProps(occurrence_uuid)

    def execute(self) -> Occurrence:
        with App.databases.create_session() as session:
            getting_repository: IFindRepository[
                OccurrenceFindRepositoryParams, Occurrence
            ] = OccurrenceFindRepository(session)

            occurrence: Occurrence = getting_repository.find_one(self.__props)

            return occurrence
