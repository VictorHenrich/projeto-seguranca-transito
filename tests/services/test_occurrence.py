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
    OccurrenceAggregationService,
)
from src.utils.entities import AddressPayload, LocationPayload, AttachmentPayload


class OccurrenceServiceCase(TestCase):
    def setUp(self) -> None:
        self.__occurrence_payload: Mock = Mock()

        attachment: AttachmentPayload = AttachmentPayload(
            b64encode("Isto aqui é apenas um teste meu amigo".encode("utf-8")),
            "text/plain",
        )

        self.__occurrence_payload.id_uuid = ""
        self.__occurrence_payload.user_uuid = "72b5a0ba-e454-4668-8965-f4901353c4e4"
        self.__occurrence_payload.vehicle_uuid = "19a9fd5c-ec15-402d-978b-11a92b9c6f75"
        self.__occurrence_payload.description = "EU BATI MEU CARRO"
        self.__occurrence_payload.address = LocationPayload(-28.4944057, -48.9936902)
        self.__occurrence_payload.created = datetime.now()
        self.__occurrence_payload.attachments = [attachment]

    def test_creation(self) -> None:
        occurrence_creation_service: IService[None] = OccurrenceCreationService(
            user_uuid=self.__occurrence_payload.user_uuid,
            vehicle_uuid=self.__occurrence_payload.vehicle_uuid,
            description=self.__occurrence_payload.description,
            address=self.__occurrence_payload.address,
            created=self.__occurrence_payload.created,
            attachments=self.__occurrence_payload.attachments,
        )

        occurrence_creation_service.execute()

    def test_exclusion(self) -> None:
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

    def test_aggregate(self) -> None:
        user_payload: Mock = Mock()

        user_payload.id = 8

        occurrences_aggregate_service: IService[
            Collection[Mapping[str, Any]]
        ] = OccurrenceAggregationService(user_payload)

        occurrences_data: Collection[
            Mapping[str, Any]
        ] = occurrences_aggregate_service.execute()

        pprint(f"===================> {occurrences_data}")

        self.assertTrue(occurrences_data)
