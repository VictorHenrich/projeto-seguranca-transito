from typing import List
from dataclasses import dataclass

from server import App
from patterns.repository import IFindManyRepository
from models import User, Occurrence
from repositories.occurrence import (
    OccurrenceFindManyRepository,
    OccurrenceFindManyRepositoryParams,
)


@dataclass
class OccurrenceListingServiceProps:
    user: User


class OccurrenceListingService:
    def execute(self, props: OccurrenceListingServiceProps) -> List[Occurrence]:
        with App.databases().create_session() as session:
            listing_repository: IFindManyRepository[
                OccurrenceFindManyRepositoryParams, Occurrence
            ] = OccurrenceFindManyRepository(session)

            occurrences: List[Occurrence] = listing_repository.list(props)

            return occurrences
