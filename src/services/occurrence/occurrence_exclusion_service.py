from dataclasses import dataclass

from server import App
from patterns.repository import IDeleteRepository
from repositories.occurrence import (
    OccurrenceDeleteRepository,
    OccurrenceDeleteRepositoryParams,
)


@dataclass
class OccurrenceExclusionServiceProps:
    uuid_occurrence: str


class OccurrenceExclusionService:
    def execute(self, props: OccurrenceExclusionServiceProps) -> None:
        with App.databases().create_session() as session:
            exclusion_repository: IDeleteRepository[
                OccurrenceDeleteRepositoryParams, None
            ] = OccurrenceDeleteRepository(session)

            exclusion_repository.delete(props)

            session.commit()
