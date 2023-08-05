from typing import Collection, Mapping, Any
from unittest import TestCase
from unittest.mock import Mock
from pprint import pprint


from src.patterns.service import IService
from src.services.vehicle import VehicleListingService


class VehicleServiceCase(TestCase):
    def setUp(self) -> None:
        self.__user: Mock = Mock()

        self.__user.id = 8

    def test_find_many(self) -> None:
        vehicle_listing_service: IService[
            Collection[Mapping[str, Any]]
        ] = VehicleListingService(self.__user)

        vehicles: Collection[Mapping[str, Any]] = vehicle_listing_service.execute()

        pprint(f"==========> {vehicles}")

        self.assertTrue(vehicles)
