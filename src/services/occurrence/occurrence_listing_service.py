from typing import List
from dataclasses import dataclass

from start import app
from patterns.repository import IFindManyRepository
from models import Usuario, Ocorrencia
from repositories.occurrence import (
    OccurrenceFindManyRepository,
    OccurrenceFindManyRepositoryParams,
)


@dataclass
class OccurrenceFindManyProps:
    user: Usuario


class OccurrenceListingService:
    def execute(self, user: Usuario) -> List[Ocorrencia]:
        with app.databases.create_session() as session:
            listing_repository_param: OccurrenceFindManyRepositoryParams = (
                OccurrenceFindManyProps(user=user)
            )

            listing_repository: IFindManyRepository[
                OccurrenceFindManyRepositoryParams, Ocorrencia
            ] = OccurrenceFindManyRepository(session)

            occurrences: List[Ocorrencia] = listing_repository.list(
                listing_repository_param
            )

            return occurrences
