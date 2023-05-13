from typing import Protocol

from patterns.repository import BaseRepository, IFindRepository
from models import Vehicle, User
from .vehicle_find_repository import VehicleFindRepository, VehicleFindRepositoryParams


class VehicleDeleteRepositoryParams(Protocol):
    vehicle_uuid: str
    user: User


class VehicleDeleteRepository(BaseRepository):
    def delete(self, params: VehicleDeleteRepositoryParams) -> None:
        vehicle_find_service: IFindRepository[
            VehicleFindRepositoryParams, Vehicle
        ] = VehicleFindRepository(self.session)

        vehicle: Vehicle = vehicle_find_service.find_one(params)

        self.session.delete(vehicle)
