from start import app
from patterns.repository import IUpdateRepository
from repositories.occurrence import (
    OccurrenceUpdateRepository,
    OccurrenceUpdateRepositoryParam
)





class OccurrenceUpdateService:
    def execute(
        self,
        uuid_occurrence: str,
        description: str,
        obs: str
    ) -> None:
        with app.databases.create_session() as session:
            update_repository_param: OccurrenceUpdateRepositoryParam = \
                OccurrenceUpdateRepositoryParam(
                    uuid_occurrence=uuid_occurrence,
                    description=description,
                    obs=obs
                )

            update_repository: IUpdateRepository[OccurrenceUpdateRepositoryParam] = \
                OccurrenceUpdateRepository(session)

            update_repository.update(update_repository_param)

            session.commit()