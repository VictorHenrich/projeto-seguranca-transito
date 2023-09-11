from typing import Collection
from datetime import date
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import Databases
from models import User
from patterns.repository import ICreateRepository
from patterns.service import IService
from repositories.user import UserCreateRepository, UserCreateRepositoryParams
from services.vehicle import VehicleCreationService
from utils.entities import AddressPayload, VehiclePayload


@dataclass
class UserCreateRepoProps:
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
        address: AddressPayload,
        vehicles: Collection[VehiclePayload],
    ):
        self.__user_create_props: UserCreateRepoProps = UserCreateRepoProps(
            name=name,
            email=email,
            password=password,
            document=document,
            birthday=birthday,
            document_rg=document_rg,
            telephone=telephone,
            state_issuer=state_issuer,
            address_state=address.state,
            address_city=address.city,
            address_district=address.district,
            address_street=address.street,
            address_number=address.number,
        )

        self.__vehicle_create_props: Collection[VehiclePayload] = vehicles

    def __create_user(self, session: Session) -> User:
        user_create_repository: ICreateRepository[
            UserCreateRepositoryParams, User
        ] = UserCreateRepository(session)

        return user_create_repository.create(self.__user_create_props)

    def __create_vehicles(self, session: Session, user: User) -> None:
        for vehicle in self.__vehicle_create_props:
            vehicle_creation_service: IService[None] = VehicleCreationService(
                user=user,
                vehicle_payload=vehicle,
                session=session,
            )

            vehicle_creation_service.execute()

    def execute(self) -> User:
        with Databases.create_session() as session:
            new_user: User = self.__create_user(session)

            self.__create_vehicles(session, new_user)

            session.commit()

            return new_user
