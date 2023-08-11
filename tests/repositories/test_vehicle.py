from typing import Collection
from unittest import TestCase
from unittest.mock import Mock
from pprint import pprint

from .database import database
from src.models import Vehicle
from src.patterns.repository import (
    ICreateRepository,
    IDeleteRepository,
    IFindRepository,
    IFindManyRepository,
    IUpdateRepository,
)
from src.repositories.vehicle import (
    VehicleCreateRepository,
    VehicleCreateRepositoryParams,
    VehicleFindRepository,
    VehicleFindRepositoryParams,
    VehicleFindManyRepository,
    VehicleFindManyRepositoryParams,
    VehicleUpdateRepository,
    VehicleUpdateRepositoryParams,
    VehicleDeleteRepository,
    VehicleDeleteRepositoryParams,
)
from src.utils.types import VehicleTypes


class VehicleRepositoryCase(TestCase):
    def setUp(self) -> None:
        self.__vehicle_payload: Mock = Mock()

        self.__user_payload: Mock = Mock()

        self.__user_payload.id = 8

        self.__vehicle_payload.user = self.__user_payload
        self.__vehicle_payload.plate = "22AABCDR"
        self.__vehicle_payload.renavam = "22222211123123"
        self.__vehicle_payload.vehicle_type = VehicleTypes.CAR
        self.__vehicle_payload.brand = "MARCA PADRÃO"
        self.__vehicle_payload.model = "MODELO PADRÃO"
        self.__vehicle_payload.color = "VERMELHO"
        self.__vehicle_payload.year = 2000
        self.__vehicle_payload.chassi = "2222222222222222222"
        self.__vehicle_payload.have_safe = False
        self.__vehicle_payload.vehicle_uuid = "0395418d-b39e-4df9-9282-0d4c3cee7935"

    def test_create(self) -> None:
        with self.__database.create_session() as session:
            vehicle_repository: ICreateRepository[
                VehicleCreateRepositoryParams, None
            ] = VehicleCreateRepository(session)

            vehicle_repository.create(self.__vehicle_payload)

            session.commit()

            pprint("VEHICLE CREATED")

    def test_find(self) -> None:
        with self.__database.create_session() as session:
            vehicle_repository: IFindRepository[
                VehicleFindRepositoryParams, Vehicle
            ] = VehicleFindRepository(session)

            vehicle_finded: Vehicle = vehicle_repository.find_one(
                self.__vehicle_payload
            )

            pprint(f"VEHICLE FINDED ====> {vehicle_finded}")

            self.assertTrue(vehicle_finded)

    def test_find_many(self) -> None:
        with self.__database.create_session() as session:
            vehicle_repository: IFindManyRepository[
                VehicleFindManyRepositoryParams, Vehicle
            ] = VehicleFindManyRepository(session)

            vehicles: Collection[Vehicle] = vehicle_repository.find_many(
                self.__vehicle_payload
            )

            pprint(f"VEHICLES FINDED ====> {vehicles}")

            self.assertTrue(vehicles)

    def test_update(self) -> None:
        with self.__database.create_session() as session:
            vehicle_repository: IUpdateRepository[
                VehicleUpdateRepositoryParams, None
            ] = VehicleUpdateRepository(session)

            vehicle_repository.update(self.__vehicle_payload)

            session.commit()

            pprint("VEHICLE UPDATED")

    def test_delete(self) -> None:
        with self.__database.create_session() as session:
            vehicle_repository: IDeleteRepository[
                VehicleDeleteRepositoryParams, None
            ] = VehicleDeleteRepository(session)

            vehicle_repository.delete(self.__vehicle_payload)

            session.commit()

            pprint("VEHICLE DELETED")
