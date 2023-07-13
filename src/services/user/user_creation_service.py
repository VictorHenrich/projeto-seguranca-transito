from typing import Collection, Mapping, Any
from datetime import date
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import App, Databases
from models import User
from patterns.repository import ICreateRepository
from patterns.service import IService
from repositories.user import UserCreateRepository, UserCreateRepositoryParams
from repositories.vehicle import VehicleTypes
from services.vehicle import VehicleCreationService


@dataclass
class UserCreateProps:
    name: str
    email: str
    password: str
    document: str
    document_rg: str
    telephone: str
    state_issuer: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    birthday: date


class UserCreationService:
    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        document: str,
        birthday: date,
        document_rg: str,
        telephone: str,
        state_issuer: str,
        address_state: str,
        address_city: str,
        address_district: str,
        address_street: str,
        address_number: str,
        vehicles: Collection[Mapping[str, Any]],
    ):
        self.__user_create_props: UserCreateProps = UserCreateProps(
            name=name,
            email=email,
            password=password,
            document=document,
            birthday=birthday,
            document_rg=document_rg,
            telephone=telephone,
            state_issuer=state_issuer,
            address_state=address_state,
            address_city=address_city,
            address_district=address_district,
            address_street=address_street,
            address_number=address_number,
        )

        self.__vehicle_create_props: Collection[Mapping[str, Any]] = vehicles

    def __create_user(self, session: Session) -> User:
        user_create_repository: ICreateRepository[
            UserCreateRepositoryParams, User
        ] = UserCreateRepository(session)

        return user_create_repository.create(self.__user_create_props)

    def __create_vehicles(self, session: Session, user: User) -> None:
        for vehicle in self.__vehicle_create_props:
            vehicle_type: VehicleTypes = VehicleTypes(vehicle["vehicle_type"].upper())

            vehicle_creation_service: IService[None] = VehicleCreationService(
                user=user,
                plate=vehicle["plate"],
                renavam=vehicle["renavam"],
                vehicle_type=vehicle_type,
                brand=vehicle.get("brand"),
                chassi=vehicle.get("chassi"),
                color=vehicle.get("color"),
                model=vehicle.get("model"),
                have_safe=vehicle.get("have_safe") or False,
                year=vehicle.get("year"),
                session=session,
            )

            vehicle_creation_service.execute()

    def execute(self) -> User:
        with Databases.create_session() as session:
            new_user: User = self.__create_user(session)

            self.__create_vehicles(session, new_user)

            session.commit()

            return new_user
