from typing import Protocol, Collection

from patterns.repository import BaseRepository
from models import Vehicle, User


class VehicleFindManyRepositoryParams(Protocol):
    user: User


class VehicleFindManyRepository(BaseRepository):
    def find_many(self, params: VehicleFindManyRepositoryParams) -> Collection[Vehicle]:
        return (
            self.session.query(Vehicle)
            .join(User, User.id == Vehicle.id_usuario)
            .filter(Vehicle.id_usuario == params.user.id)
            .all()
        )
