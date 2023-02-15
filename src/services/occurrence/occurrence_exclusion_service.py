from start import app
from patterns.repository import IExclusionRepository
from repositories.occurrence import (
    OccurrenceExclusionRepository,
    OccurrenceExclusionRepositoryParam,
)


class OccurrenceExclusionService:
    def execute(self, uuid_occurrence: str) -> None:
        with app.databases.create_session() as session:
            exclusion_repository_param: OccurrenceExclusionRepositoryParam = (
                OccurrenceExclusionRepositoryParam(uuid_occurrence=uuid_occurrence)
            )

            exclusion_repository: IExclusionRepository[
                OccurrenceExclusionRepositoryParam
            ] = OccurrenceExclusionRepository(session)

            exclusion_repository.delete(exclusion_repository_param)

            session.commit()
