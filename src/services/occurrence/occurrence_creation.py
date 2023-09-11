from decimal import Decimal
from typing import Optional, Mapping, Any, Collection, Tuple, Union
from dataclasses import dataclass
from sqlalchemy.orm import Session
from datetime import datetime
import json
import logging

from server import Databases, AMQPServer
from patterns.repository import ICreateRepository, IFindRepository
from patterns.service import IService
from models import User, Vehicle, Occurrence
from utils.entities import AddressPayload, LocationPayload, AttachmentPayload
from repositories.occurrence import (
    OccurrenceCreateRepository,
    OccurrenceCreateRepositoryParams,
)
from repositories.user import UserFindRepository, UserFindRepositoryParams
from repositories.vehicle import VehicleFindRepository, VehicleFindRepositoryParams
from services.integrations import GeocodingService
from services.attachment import AttachmentCreationService
from consumers.consumer_occurrences_integration import (
    EXCHANGE_OCCURRENCE_INTEGRATION_NAME,
    ROUTING_KEY_OCCURRENCE_INTEGRATION_NAME,
)


@dataclass
class OccurrenceCreationProps:
    user: User
    vehicle: Vehicle
    description: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    lat: str
    lon: str
    obs: str
    created: datetime


@dataclass
class UserFindProps:
    user_uuid: str


@dataclass
class VehicleFindProps:
    user: User
    vehicle_uuid: str


class OccurrenceCreationService:
    def __init__(
        self,
        user_uuid: str,
        vehicle_uuid: str,
        description: str,
        address: Union[AddressPayload, LocationPayload],
        created: datetime,
        attachments: Collection[AttachmentPayload],
        obs: str = "",
    ) -> None:
        self.__user_uuid: str = user_uuid
        self.__vehicle_uuid: str = vehicle_uuid
        self.__description: str = description
        self.__address: Union[AddressPayload, LocationPayload] = address
        self.__created: datetime = created
        self.__attachments: Collection[AttachmentPayload] = attachments
        self.__obs: str = obs

    def __find_user(self, session: Session) -> User:
        user_find_repository: IFindRepository[
            UserFindRepositoryParams, User
        ] = UserFindRepository(session)

        user: User = user_find_repository.find_one(UserFindProps(self.__user_uuid))

        logging.info(f"Usuario localizado: {user}")

        return user

    def __find_vehicle(self, session: Session, user: User) -> Vehicle:
        vehicle_find_repository: IFindRepository[
            VehicleFindRepositoryParams, Vehicle
        ] = VehicleFindRepository(session)

        vehicle: Vehicle = vehicle_find_repository.find_one(
            VehicleFindProps(user, self.__vehicle_uuid)
        )

        logging.info(f"veículo localizado: {vehicle}")

        return vehicle

    def __find_address(self) -> AddressPayload:
        if isinstance(self.__address, AddressPayload):
            return self.__address

        geolocation_service: IService[AddressPayload] = GeocodingService(
            self.__address.lat, self.__address.lon
        )

        geolocation_payload: AddressPayload = geolocation_service.execute()

        logging.info(f"Dados Endereço da Ocorrência: {geolocation_payload}")

        return geolocation_payload

    def __get_location(self) -> Tuple[Decimal, Decimal]:
        if isinstance(self.__address, LocationPayload):
            return Decimal(self.__address.lat), Decimal(self.__address.lon)

        else:
            return Decimal(0), Decimal(0)

    def __create_occurrence(
        self, session: Session, user: User, vehicle: Vehicle, address: AddressPayload
    ) -> Occurrence:
        occurrence_creation_repository: ICreateRepository[
            OccurrenceCreateRepositoryParams, Occurrence
        ] = OccurrenceCreateRepository(session)

        lat, lon = self.__get_location()

        return occurrence_creation_repository.create(
            OccurrenceCreationProps(
                user,
                vehicle,
                self.__description,
                address.state,
                address.city,
                address.district,
                address.street,
                "0",
                str(lat),
                str(lon),
                self.__obs,
                self.__created,
            )
        )

    def __create_attachments(self, session: Session, occurrence: Occurrence) -> None:
        attachment_create_service: IService[None] = AttachmentCreationService(
            occurrence, *self.__attachments, session=session
        )

        attachment_create_service.execute()

    def execute(self) -> None:
        occurrence: Optional[Occurrence] = None

        with Databases.create_session() as session:
            user: User = self.__find_user(session)

            vehicle: Vehicle = self.__find_vehicle(session, user)

            address: AddressPayload = self.__find_address()

            occurrence = self.__create_occurrence(session, user, vehicle, address)

            self.__create_attachments(session, occurrence)

            session.commit()

            if not occurrence:
                raise Exception("Falha ao cadastrar ocorrência!")

            consumer_payload: Mapping[str, Any] = {
                "user_uuid": user.id_uuid,
                "vehicle_uuid": vehicle.id_uuid,
                "occurrence_uuid": occurrence.id_uuid,
            }

            AMQPServer.create_publisher(
                "publisher_occurrence_integration",
                exchange=EXCHANGE_OCCURRENCE_INTEGRATION_NAME,
                routing_key=ROUTING_KEY_OCCURRENCE_INTEGRATION_NAME,
                body=json.dumps(consumer_payload).encode("utf-8"),
            )
