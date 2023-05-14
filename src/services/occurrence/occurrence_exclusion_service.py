from dataclasses import dataclass

from server import App
from patterns.repository import IDeleteRepository
from repositories.occurrence import (
    OccurrenceDeleteRepository,
    OccurrenceDeleteRepositoryParams,
)


@dataclass
class OccurrenceDeleteProps:
    occurrence_uuid: str


class OccurrenceExclusionService:
    def __init__(self, occurrence_uuid: str) -> None:
        self.__props: OccurrenceDeleteProps = OccurrenceDeleteProps(occurrence_uuid)

    def execute(self) -> None:
        with App.databases.create_session() as session:
            exclusion_repository: IDeleteRepository[
                OccurrenceDeleteRepositoryParams, None
            ] = OccurrenceDeleteRepository(session)

            exclusion_repository.delete(self.__props)

            session.commit()
