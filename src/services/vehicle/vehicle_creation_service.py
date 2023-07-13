from typing import Optional, TypeAlias
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import Databases
from models import User
from patterns.repository import ICreateRepository
from repositories.vehicle import (
    VehicleTypes,
    VehicleCreateRepository,
    VehicleCreateRepositoryParams,
)


@dataclass
class VehicleCreateProps:
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
        plate: str,
        renavam: str,
        vehicle_type: TypeAlias,
        brand: Optional[str] = None,
        model: Optional[str] = None,
        color: Optional[str] = None,
        year: Optional[str] = None,
        chassi: Optional[str] = None,
        have_safe: bool = False,
        session: Optional[Session] = None,
    ) -> None:
        self.__props: VehicleCreateProps = VehicleCreateProps(
            user,
            plate,
            renavam,
            vehicle_type,
            brand,
            model,
            color,
            year,
            chassi,
            have_safe,
        )

        self.__session: Optional[Session] = session

    def __create_vehicle(self, session: Session) -> None:
        vehicle_create_repository: ICreateRepository[
            VehicleCreateRepositoryParams, None
        ] = VehicleCreateRepository(session)

        vehicle_create_repository.create(self.__props)

    def execute(self) -> None:
        if self.__session:
            self.__create_vehicle(self.__session)

        else:
            with Databases.create_session() as session:
                self.__create_vehicle(session)

                session.commit()
