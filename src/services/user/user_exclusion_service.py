from typing import Collection
from dataclasses import dataclass

from server import App
from patterns.repository import IFindManyRepository, IFindRepository
from models import User, Vehicle
from repositories.user import UserFindRepository, UserFindRepositoryParams
from repositories.vehicle import (
    VehicleFindManyRepository,
    VehicleFindManyRepositoryParams,
)


@dataclass
class UserFindProps:
    user_uuid: str


@dataclass
class VehicleFindManyProps:
    user: User


class UserExclusionService:
    def __init__(self, user_uuid: str) -> None:
        self.__user_uuid: str = user_uuid

    def execute(self) -> None:
        with App.databases.create_session() as session:
            user_find_repo: IFindRepository[
                UserFindRepositoryParams, User
            ] = UserFindRepository(session)

            vehicle_find_many_repo: IFindManyRepository[
                VehicleFindManyRepositoryParams, Vehicle
            ] = VehicleFindManyRepository(session)

            user: User = user_find_repo.find_one(UserFindProps(self.__user_uuid))

            vehicles: Collection[Vehicle] = vehicle_find_many_repo.find_many(
                VehicleFindManyProps(user)
            )

            for vehicle in vehicles:
                session.delete(vehicle)

            session.delete(user)

            session.commit()
