from typing import Protocol, Sequence

from patterns.repository import BaseRepository
from models import Vehicle


class VehicleFindRepositoryParams(Protocol):
    vehicle_uuid: str


class VehicleFindManyRepository(BaseRepository):
    def find_many(self, params: VehicleFindRepositoryParams) -> Sequence[Vehicle]:
        return (
            self.session.query(Vehicle)
            .filter(Vehicle.id_uuid == params.vehicle_uuid)
            .all()
        )
