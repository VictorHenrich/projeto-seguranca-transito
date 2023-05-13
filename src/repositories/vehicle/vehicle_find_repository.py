from typing import Protocol, Optional

from patterns.repository import BaseRepository
from models import Vehicle


class VehicleFindRepositoryParams(Protocol):
    vehicle_uuid: str


class VehicleFindRepository(BaseRepository):
    def find_one(self, params: VehicleFindRepositoryParams) -> Vehicle:
        vehicle: Optional[Vehicle] = (
            self.session.query(Vehicle)
            .filter(Vehicle.id_uuid == params.vehicle_uuid)
            .first()
        )

        if not vehicle:
            raise Exception("Veículo não localizado!")

        return vehicle
