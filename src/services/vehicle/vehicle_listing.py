from typing import Collection
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server.database import Databases
from models import Vehicle, User
from patterns.repository import IFindManyRepository
from repositories.vehicle import (
    VehicleFindManyRepository,
    VehicleFindManyRepositoryParams,
)
from utils.types import DictType


@dataclass
class VehicleProps:
    user: User


class VehicleListingService:
    def __init__(self, user: User) -> None:
        self.__props: VehicleProps = VehicleProps(user)

    def __find_vehicles(self, session: Session) -> Collection[Vehicle]:
        vehicle_find_many_repo: IFindManyRepository[
            VehicleFindManyRepositoryParams, Vehicle
        ] = VehicleFindManyRepository(session)

        return vehicle_find_many_repo.find_many(self.__props)

    def __handle_vehicle(self, vehicle: Vehicle) -> DictType:
        return {
            "uuid": vehicle.id_uuid,
            "plate": vehicle.placa,
            "renavam": vehicle.renavam,
            "type": vehicle.tipo_veiculo,
            "color": vehicle.cor,
            "year": vehicle.ano,
            "brand": vehicle.marca,
            "model": vehicle.modelo,
            "have_safe": vehicle.possui_seguro,
        }

    def execute(self) -> Collection[DictType]:
        with Databases.create_session() as session:
            vehicles: Collection[Vehicle] = self.__find_vehicles(session)

            return [self.__handle_vehicle(vehicle) for vehicle in vehicles]
