from typing import Optional
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import Databases
from models import User, Vehicle
from patterns.repository import ICreateRepository
from repositories.vehicle import (
    VehicleCreateRepository,
    VehicleCreateRepositoryParams,
)
from utils.entities import VehiclePayload
from utils.types import VehicleTypes, DictType


@dataclass
class VehicleCreateRepoProps:
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


class VehicleCreationService:
    def __init__(
        self,
        user: User,
        vehicle_payload: VehiclePayload,
        session: Optional[Session] = None,
    ) -> None:
        self.__props: VehicleCreateRepoProps = VehicleCreateRepoProps(
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

        self.__session: Optional[Session] = session

    def __create_vehicle(self, session: Session) -> DictType:
        vehicle_create_repository: ICreateRepository[
            VehicleCreateRepositoryParams, Vehicle
        ] = VehicleCreateRepository(session)

        vehicle: Vehicle = vehicle_create_repository.create(self.__props)

        return self.__handle_vehicle(vehicle)

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

    def execute(self) -> DictType:
        if self.__session:
            return self.__create_vehicle(self.__session)

        else:
            with Databases.create_session() as session:
                vehicle: DictType = self.__create_vehicle(session)

                session.commit()

                return vehicle
