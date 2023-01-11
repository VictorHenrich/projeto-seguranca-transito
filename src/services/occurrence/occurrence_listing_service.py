from typing import List

from start import app
from patterns.repository import IListingRepository
from models import Usuario, Ocorrencia
from repositories.occurrence import (
    OccurrenceListingRepository,
    OccurrenceListingRepositoryParam
)



class OccurrenceListingService:
    def execute(
        self,
        user: Usuario
    ) -> List[Ocorrencia]:
        with app.databases.create_session() as session:
            listing_repository_param: OccurrenceListingRepositoryParam = \
                OccurrenceListingRepositoryParam(user=user)

            listing_repository: IListingRepository[OccurrenceListingRepositoryParam, Ocorrencia] = \
                OccurrenceListingRepository(session)

            occurrences: List[Ocorrencia] = listing_repository.list(listing_repository_param)

            return occurrences