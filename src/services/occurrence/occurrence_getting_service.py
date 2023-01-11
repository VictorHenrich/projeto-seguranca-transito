from start import app
from patterns.repository import IGettingRepository
from models import Ocorrencia
from repositories.occurrence import (
    OccurrenceGettingRepository,
    OccurrenceGettingRepositoryParam
)



class OccurrenceGettingService:
    def execute(
        self,
        uuid_occurrence: str
    ) -> Ocorrencia:
        with app.databases.create_session() as session:
            getting_repository_param: OccurrenceGettingRepositoryParam = \
                OccurrenceGettingRepositoryParam(uuid_occurrence=uuid_occurrence)

            getting_repository: IGettingRepository[OccurrenceGettingRepositoryParam, Ocorrencia] =\
                OccurrenceGettingRepository(session)

            occurrence: Ocorrencia = getting_repository.get(getting_repository_param)

            return occurrence