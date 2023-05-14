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
class OccurrenceFindManyProps:
    user: User


class OccurrenceListingService:
    def __init__(self, user: User) -> None:
        self.__props: OccurrenceFindManyProps = OccurrenceFindManyProps(user)

    def execute(self) -> List[Occurrence]:
        with App.databases.create_session() as session:
            listing_repository: IFindManyRepository[
                OccurrenceFindManyRepositoryParams, Occurrence
            ] = OccurrenceFindManyRepository(session)

            occurrences: List[Occurrence] = listing_repository.find_many(self.__props)

            return occurrences
