from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime

from ..util import TestUtil

TestUtil.load_modules()

import src.main
from src.patterns.service import IService
from src.services.occurrence import OccurrenceCreationService


class OccurrenceServiceCase(TestCase):
    def setUp(self) -> None:
        self.__occurrence_payload: Mock = Mock()

        self.__occurrence_payload.user_uuid = "e3eb578a-f643-482d-ac73-f290b70041d5"
        self.__occurrence_payload.vehicle_uuid = "48b5cbd1-928e-4ce1-94c6-e7b57ed8dc3a"
        self.__occurrence_payload.description = "EU BATI MEU CARRO"
        self.__occurrence_payload.lat = -28.4400207
        self.__occurrence_payload.lon = -48.9545278
        self.__occurrence_payload.created = datetime.now()

    def test_creation(self) -> None:
        occurrence_creation_service: IService[None] = OccurrenceCreationService(
            user_uuid=self.__occurrence_payload.user_uuid,
            vehicle_uuid=self.__occurrence_payload.vehicle_uuid,
            description=self.__occurrence_payload.description,
            lat=self.__occurrence_payload.lat,
            lon=self.__occurrence_payload.lon,
            created=self.__occurrence_payload.created,
        )

        occurrence_creation_service.execute()
