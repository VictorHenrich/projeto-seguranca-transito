from typing import List
from dataclasses import dataclass

from start import app
from patterns.repository import IFindManyRepository
from models import User, Occurrence
from repositories.occurrence import (
    OccurrenceFindManyRepository,
    OccurrenceFindManyRepositoryParams,
)


@dataclass
class OccurrenceFindManyProps:
    user: User


class OccurrenceListingService:
    def execute(self, user: User) -> List[Occurrence]:
        with app.databases.create_session() as session:
            listing_repository_param: OccurrenceFindManyRepositoryParams = (
                OccurrenceFindManyProps(user=user)
            )

            listing_repository: IFindManyRepository[
                OccurrenceFindManyRepositoryParams, Occurrence
            ] = OccurrenceFindManyRepository(session)

            occurrences: List[Occurrence] = listing_repository.list(
                listing_repository_param
            )

            return occurrences
