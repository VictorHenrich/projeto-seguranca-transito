from typing import Optional, Collection, Mapping, Any, Literal
from datetime import date
from dataclasses import dataclass
from sqlalchemy.orm import Session
import logging

from server import App
from models import User
from patterns.repository import ICreateRepository
from patterns.service import IService
from .user_authentication_service import UserAuthenticationService
from repositories.user import UserCreateRepository, UserCreateRepositoryParams
from repositories.vehicle import VehicleCreateRepository, VehicleCreateRepositoryParams


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


@dataclass
class VehicleCreateProps:
    user: User
    plate: str
    renavam: str
    vehicle_type: Literal["CARRO", "MOTO"]
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    chassi: Optional[str] = None
    have_safe: bool = False


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
            vehicle_create_props: VehicleCreateProps = VehicleCreateProps(
                user=user,
                plate=vehicle["plate"],
                renavam=vehicle["renavam"],
                vehicle_type=vehicle["vehicle_type"],
                brand=vehicle.get("brand"),
                chassi=vehicle.get("chassi"),
                color=vehicle.get("color"),
                model=vehicle.get("model"),
                have_safe=vehicle.get("have_safe") or False,
                year=vehicle.get("year"),
            )

            vehicle_create_repository: ICreateRepository[
                VehicleCreateRepositoryParams, None
            ] = VehicleCreateRepository(session)

            vehicle_create_repository.create(vehicle_create_props)

    def __authenticate(self, session: Session, user: User) -> str:
        user_auth_service: IService[str] = UserAuthenticationService(
            email=user.email,
            password=user.senha,
            session=session
        )

        return user_auth_service.execute()

    def execute(self) -> str:
        with App.databases.create_session() as session:
            new_user: User = self.__create_user(session)

            logging.info(f"USUÁRIO CRIADO: {new_user.id_uuid}")

            self.__create_vehicles(session, new_user)

            token: str = self.__authenticate(session, new_user)

            logging.info(f"TOKEN CRIADO: {token}")

            session.commit()

            return token
