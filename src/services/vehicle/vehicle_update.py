from typing import Optional, Mapping, Any
from dataclasses import dataclass

from server.database import Databases
from models import User, Vehicle
from repositories.vehicle import VehicleUpdateRepository, VehicleUpdateRepositoryParams
from patterns.repository import IUpdateRepository
from utils.entities import VehiclePayload
from utils.types import VehicleTypes, DictType


@dataclass
class VehicleUpdateProps:
    vehicle_uuid: str
    user: User
    plate: str
    renavam: str
    vehicle_type: VehicleTypes
    brand: Optional[str]
    model: Optional[str]
    color: Optional[str]
    year: Optional[int]
    chassi: Optional[str]
    have_safe: bool


class VehicleUpdateService:
    def __init__(
        self, vehicle_uuid: str, user: User, vehicle_payload: VehiclePayload
    ) -> None:
        self.__vehicle_props = VehicleUpdateProps(
            vehicle_uuid,
            user,
            vehicle_payload.plate,
            vehicle_payload.renavam,
            vehicle_payload.vehicle_type,
            vehicle_payload.brand,
            vehicle_payload.model,
            vehicle_payload.color,
            vehicle_payload.year,
            vehicle_payload.chassi,
            vehicle_payload.have_safe,
        )

    def __handle_vehicle(self, vehicle: Vehicle) -> DictType:
        return {
            "uuid": vehicle.id_uuid,
            "plate": vehicle.placa,
            "renavam": vehicle.renavam,
            "vehicle_type": vehicle.tipo_veiculo,
            "chassi": vehicle.chassi,
            "brand": vehicle.marca,
            "model": vehicle.modelo,
            "year": vehicle.ano,
            "have_safe": vehicle.possui_seguro,
        }

    def __update(self) -> DictType:
        with Databases.create_session() as session:
            vehicle_update_repo: IUpdateRepository[
                VehicleUpdateRepositoryParams, Vehicle
            ] = VehicleUpdateRepository(session)

            vehicle: Vehicle = vehicle_update_repo.update(self.__vehicle_props)

            session.commit()

            return self.__handle_vehicle(vehicle)

    def execute(self) -> DictType:
        return self.__update()
