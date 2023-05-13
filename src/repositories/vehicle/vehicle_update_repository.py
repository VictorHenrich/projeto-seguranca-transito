from typing import Protocol, Literal, Optional

from patterns.repository import BaseRepository, IFindRepository
from models import Vehicle, User
from .vehicle_find_repository import VehicleFindRepository, VehicleFindRepositoryParams


class VehicleUpdateRepositoryParams(Protocol):
    vehicle_uuid: str
    user: User
    plate: str
    renavam: str
    vehicle_type: Literal["AUTOMOVEL", "MOTOCICLETA"]
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    chassi: Optional[str] = None
    have_safe: bool = False


class VehicleUpdateRepository(BaseRepository):
    def update(self, params: VehicleUpdateRepositoryParams) -> None:
        vehicle_find_service: IFindRepository[
            VehicleFindRepositoryParams, Vehicle
        ] = VehicleFindRepository(self.session)

        vehicle: Vehicle = vehicle_find_service.find_one(params)

        vehicle.placa = params.plate
        vehicle.renavam = params.renavam
        vehicle.tipo_veiculo = params.vehicle_type
        vehicle.marca = params.brand
        vehicle.modelo = params.model
        vehicle.cor = params.color
        vehicle.ano = params.year
        vehicle.chassi = params.chassi
        vehicle.possui_seguro = params.have_safe

        self.session.add(vehicle)
