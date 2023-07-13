from typing import Mapping, Any, Collection
from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime
from base64 import b64encode
from pprint import pprint

from src.patterns.service import IService
from src.services.occurrence import (
    OccurrenceCreationService,
    OccurrenceExclusionService,
    OccurrenceGettingService,
    OccurrenceListingService,
)


class OccurrenceServiceCase(TestCase):
    def setUp(self) -> None:
        self.__occurrence_payload: Mock = Mock()

        self.__occurrence_payload.id_uuid = ""
        self.__occurrence_payload.user_uuid = "e3eb578a-f643-482d-ac73-f290b70041d5"
        self.__occurrence_payload.vehicle_uuid = "48b5cbd1-928e-4ce1-94c6-e7b57ed8dc3a"
        self.__occurrence_payload.description = "EU BATI MEU CARRO"
        self.__occurrence_payload.lat = -28.4400207
        self.__occurrence_payload.lon = -48.9545278
        self.__occurrence_payload.created = datetime.now()
        self.__occurrence_payload.attachments = [
            {
                "content": b64encode(
                    "Isto aqui é apenas um teste meu amigo".encode("utf-8")
                ),
                "type": "text/plain",
            }
        ]

    def __test_creation(self) -> None:
        occurrence_creation_service: IService[None] = OccurrenceCreationService(
            user_uuid=self.__occurrence_payload.user_uuid,
            vehicle_uuid=self.__occurrence_payload.vehicle_uuid,
            description=self.__occurrence_payload.description,
            lat=self.__occurrence_payload.lat,
            lon=self.__occurrence_payload.lon,
            created=self.__occurrence_payload.created,
            attachments=self.__occurrence_payload.attachments,
        )

        occurrence_creation_service.execute()

    def __test_exclusion(self) -> None:
        occurrence_exclusion_service: IService[None] = OccurrenceExclusionService(
            self.__occurrence_payload.id_uuid
        )

        occurrence_exclusion_service.execute()

    def test_get(self) -> None:
        occurrence_get_service: IService[Mapping[str, Any]] = OccurrenceGettingService(
            self.__occurrence_payload.id_uuid
        )

        occurrence_data: Mapping[str, Any] = occurrence_get_service.execute()

        pprint(f"===================> {occurrence_data}")

        self.assertTrue(occurrence_data)

    def test_list(self) -> None:
        user_payload: Mock = Mock()

        user_payload.id = 1

        occurrence_get_service: IService[
            Collection[Mapping[str, Any]]
        ] = OccurrenceListingService(user_payload)

        occurrences_data: Collection[
            Mapping[str, Any]
        ] = occurrence_get_service.execute()

        pprint(f"===================> {occurrences_data}")

        self.assertTrue(occurrences_data)
