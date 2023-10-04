from typing import Collection, Mapping, Any
from unittest import TestCase
from unittest.mock import Mock
from pprint import pprint

from src.patterns.service import IService
from src.services.vehicle import (
    VehicleListingService,
    VehicleUpdateService,
    VehicleCreationService,
    VehicleExclusionService,
)
from src.utils.entities import VehiclePayload
from src.utils.types import VehicleTypes


class VehicleServiceCase(TestCase):
    def setUp(self) -> None:
        self.__user: Mock = Mock()

        self.__vehicle: Mock = Mock()

        self.__vehicle_payload: VehiclePayload = VehiclePayload(
            "11111111", "22222222", VehicleTypes.MOTOR
        )

        self.__vehicle.id_uuid = "4640d1fd-33d7-47a3-94ef-8aaf4b3ec9c9"

        self.__user.id = 2

    def test_find_many(self) -> None:
        vehicle_listing_service: IService[
            Collection[Mapping[str, Any]]
        ] = VehicleListingService(self.__user)

        vehicles: Collection[Mapping[str, Any]] = vehicle_listing_service.execute()

        pprint(f"Veículos: {vehicles}")

        self.assertTrue(vehicles)

    def test_create(self) -> None:
        vehicle_create_service: IService[Mapping[str, Any]] = VehicleCreationService(
            self.__user, self.__vehicle_payload
        )

        vehicle_created: Mapping[str, Any] = vehicle_create_service.execute()

        pprint(f"veículo Criado: {vehicle_created}")

    def test_update(self) -> None:
        vehicle_update_service: IService[Mapping[str, Any]] = VehicleUpdateService(
            self.__vehicle.id_uuid, self.__user, self.__vehicle_payload
        )

        vehicle_update: Mapping[str, Any] = vehicle_update_service.execute()

        pprint(f"Veículo Atualizado: {vehicle_update}")

    def test_delete(self) -> None:
        vehicle_exclusion_service: IService[None] = VehicleExclusionService(
            self.__vehicle.id_uuid, self.__user
        )

        vehicle_exclusion_service.execute()

        pprint(f"Veículo {self.__vehicle.id_uuid} excluído com sucesso")
