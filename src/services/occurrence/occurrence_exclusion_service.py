from dataclasses import dataclass

from start import app
from patterns.repository import IDeleteRepository
from repositories.occurrence import (
    OccurrenceDeleteRepository,
    OccurrenceDeleteRepositoryParams,
)


@dataclass
class OccurrenceDeleteProps:
    uuid_occurrence: str


class OccurrenceExclusionService:
    def execute(self, uuid_occurrence: str) -> None:
        with app.databases.create_session() as session:
            exclusion_repository_param: OccurrenceDeleteRepositoryParams = (
                OccurrenceDeleteProps(uuid_occurrence=uuid_occurrence)
            )

            exclusion_repository: IDeleteRepository[
                OccurrenceDeleteRepositoryParams
            ] = OccurrenceDeleteRepository(session)

            exclusion_repository.delete(exclusion_repository_param)

            session.commit()
