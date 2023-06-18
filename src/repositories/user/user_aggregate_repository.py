from typing import Collection, Optional, Protocol, Tuple, TypeAlias
from dataclasses import dataclass

from patterns.repository import BaseRepository, IFindManyRepository
from models import User, Vehicle, Occurrence
from exceptions import UserNotFoundError
from repositories.vehicle import (
    VehicleFindManyRepository,
    VehicleFindManyRepositoryParams,
)
from repositories.occurrence import (
    OccurrenceFindManyRepository,
    OccurrenceFindManyRepositoryParams,
)


UserLoad: TypeAlias = Tuple[User, Collection[Vehicle], Collection[Occurrence]]


class UserAggregateRepositoryParams(Protocol):
    user_uuid: str


@dataclass
class UserParams:
    user: User


class UserAggregateRepository(BaseRepository):
    def __find_vehicles(self, user_params: UserParams) -> Collection[Vehicle]:
        vehicle_find_many: IFindManyRepository[
            VehicleFindManyRepositoryParams, Vehicle
        ] = VehicleFindManyRepository(self.session)

        return vehicle_find_many.find_many(user_params)

    def __find_occurrences(self, user_params: UserParams) -> Collection[Occurrence]:
        occurrence_find_many: IFindManyRepository[
            OccurrenceFindManyRepositoryParams, Occurrence
        ] = OccurrenceFindManyRepository(self.session)

        return occurrence_find_many.find_many(user_params)

    def aggregate(self, params: UserAggregateRepositoryParams) -> UserLoad:
        user: Optional[User] = (
            self.session.query(User).filter(User.id_uuid == params.user_uuid).first()
        )

        if not user:
            raise UserNotFoundError()

        user_params: UserParams = UserParams(user)

        vehicles: Collection[Vehicle] = self.__find_vehicles(user_params)

        occurrences: Collection[Occurrence] = self.__find_occurrences(user_params)

        return user, vehicles, occurrences
