from typing import Protocol, Optional

from patterns.repository import BaseRepository
from models import Vehicle, User


class VehicleFindRepositoryParams(Protocol):
    user: User
    vehicle_uuid: str


class VehicleFindRepository(BaseRepository):
    def find_one(self, params: VehicleFindRepositoryParams) -> Vehicle:
        vehicle: Optional[Vehicle] = (
            self.session.query(Vehicle)
            .join(User, User.id == Vehicle.id_usuario)
            .filter(Vehicle.id_uuid == params.vehicle_uuid, User.id == params.user.id)
            .first()
        )

        if not vehicle:
            raise Exception("Veículo não localizado!")

        return vehicle
