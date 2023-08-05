from typing import Collection, Mapping, Any
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server.database import Databases
from models import Vehicle, User
from patterns.repository import IFindManyRepository
from repositories.vehicle import (
    VehicleFindManyRepository,
    VehicleFindManyRepositoryParams,
)


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

    def __handle_vehicle(self, vehicle: Vehicle) -> Mapping[str, Any]:
        return {
            "uuid": vehicle.id_uuid,
            "placa": vehicle.placa,
            "renavam": vehicle.renavam,
            "tipo_veiculo": vehicle.tipo_veiculo,
            "cor": vehicle.cor,
            "ano": vehicle.ano,
            "marca": vehicle.marca,
            "modelo": vehicle.modelo,
            "possui_seguro": vehicle.possui_seguro,
        }

    def execute(self) -> Collection[Mapping[str, Any]]:
        with Databases.create_session() as session:
            vehicles: Collection[Vehicle] = self.__find_vehicles(session)

            return [self.__handle_vehicle(vehicle) for vehicle in vehicles]
