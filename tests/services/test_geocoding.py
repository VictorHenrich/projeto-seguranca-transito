from unittest import TestCase
from unittest.mock import Mock

from src.patterns.service import IService
from src.services.integrations import GeocodingService
from src.utils.entities import AddressPayload


class GeocodingServiceCase(TestCase):
    def test_search(self):
        geocoding_payload: Mock = Mock()

        geocoding_payload.lat = -28.4400207
        geocoding_payload.lon = -48.9545278

        geocoding_service: IService[AddressPayload] = GeocodingService(
            geocoding_payload.lat, geocoding_payload.lon
        )

        data: AddressPayload = geocoding_service.execute()

        print("=============> ", data)

        self.assertTrue(data)
