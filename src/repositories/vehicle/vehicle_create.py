from typing import Protocol, Optional

from patterns.repository import BaseRepository
from models import Vehicle, User
from utils.types import VehicleTypes


class VehicleCreateRepositoryParams(Protocol):
    user: User
    plate: str
    renavam: str
    vehicle_type: VehicleTypes
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    chassi: Optional[str] = None
    have_safe: bool = False


class VehicleCreateRepository(BaseRepository):
    def create(self, params: VehicleCreateRepositoryParams) -> Vehicle:
        vehicle: Vehicle = Vehicle()

        vehicle.id_usuario = params.user.id
        vehicle.placa = params.plate
        vehicle.renavam = params.renavam
        vehicle.tipo_veiculo = params.vehicle_type.value
        vehicle.marca = params.brand
        vehicle.modelo = params.model
        vehicle.cor = params.color
        vehicle.ano = params.year
        vehicle.chassi = params.chassi
        vehicle.possui_seguro = params.have_safe

        self.session.add(vehicle)
        self.session.flush()

        return vehicle
