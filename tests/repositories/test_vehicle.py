from typing import Collection
from unittest import TestCase
from unittest.mock import Mock
from pprint import pprint

from src.server import App
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


class VehicleRepositoryCase(TestCase):
    def setUp(self) -> None:
        self.__vehicle_payload: Mock = Mock()

        self.__user_payload: Mock = Mock()

        self.__user_payload.id = 1

        self.__vehicle_payload.user = self.__user_payload
        self.__vehicle_payload.plate = "111AA222CV333"
        self.__vehicle_payload.renavam = "122BBNTR"
        self.__vehicle_payload.vehicle_type = "CARRO"
        self.__vehicle_payload.brand = "ALGUMA MARCA"
        self.__vehicle_payload.model = "ALGUM MODELO"
        self.__vehicle_payload.color = "ROSA"
        self.__vehicle_payload.year = 2020
        self.__vehicle_payload.chassi = ""
        self.__vehicle_payload.have_safe = False
        self.__vehicle_payload.vehicle_uuid = ""

    def test_create(self) -> None:
        with App.databases.create_session() as session:
            vehicle_repository: ICreateRepository[
                VehicleCreateRepositoryParams, None
            ] = VehicleCreateRepository(session)

            vehicle_repository.create(self.__vehicle_payload)

            pprint("VEHICLE CREATED")

    def test_find(self) -> None:
        with App.databases.create_session() as session:
            vehicle_repository: IFindRepository[
                VehicleFindRepositoryParams, Vehicle
            ] = VehicleFindRepository(session)

            vehicle_finded: Vehicle = vehicle_repository.find_one(
                self.__vehicle_payload
            )

            pprint(f"VEHICLE FINDED ====> {vehicle_finded}")

            self.assertTrue(vehicle_finded)

    def test_find_many(self) -> None:
        with App.databases.create_session() as session:
            vehicle_repository: IFindManyRepository[
                VehicleFindManyRepositoryParams, Vehicle
            ] = VehicleFindManyRepository(session)

            vehicles: Collection[Vehicle] = vehicle_repository.find_many(
                self.__vehicle_payload
            )

            pprint(f"VEHICLES FINDED ====> {vehicles}")

            self.assertTrue(vehicles)

    def test_update(self) -> None:
        with App.databases.create_session() as session:
            vehicle_repository: IUpdateRepository[
                VehicleUpdateRepositoryParams, None
            ] = VehicleUpdateRepository(session)

            vehicle_repository.update(self.__vehicle_payload)

            pprint("VEHICLE UPDATED")

    def test_delete(self) -> None:
        with App.databases.create_session() as session:
            vehicle_repository: IDeleteRepository[
                VehicleDeleteRepositoryParams, None
            ] = VehicleDeleteRepository(session)

            vehicle_repository.delete(self.__vehicle_payload)

            pprint("VEHICLE DELETED")
