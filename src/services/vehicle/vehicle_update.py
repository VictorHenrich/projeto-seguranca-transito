from typing import Optional
from dataclasses import dataclass

from server.database import Databases
from models import User
from repositories.vehicle import VehicleUpdateRepository, VehicleUpdateRepositoryParams
from patterns.repository import IUpdateRepository
from utils.entities import VehiclePayload
from utils.types import VehicleTypes


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

    def execute(self) -> None:
        with Databases.create_session() as session:
            vehicle_update_repo: IUpdateRepository[
                VehicleUpdateRepositoryParams, None
            ] = VehicleUpdateRepository(session)

            vehicle_update_repo.update(self.__vehicle_props)
