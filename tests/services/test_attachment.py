from typing import Mapping, Any
from unittest import TestCase
from unittest.mock import Mock
from base64 import b64encode
from pprint import pprint

from ..util import TestUtil

TestUtil.load_modules()

import src.main
from src.patterns.service import IService
from src.services.attachment import AttachmentCreationService, AttachmentGettingService


class AttachmentServiceCase(TestCase):
    def setUp(self) -> None:
        self.__occurrence_payload: Mock = Mock()

        self.__attachment_payload: Mock = Mock()

        self.__occurrence_payload.id = 1

        self.__attachment_payload.id_uuid = "008ab7fc-4d7b-422a-8013-eadccad40865"

        self.__attachment_payload.attachments = [
            {
                "content": b64encode(
                    "Estou apenas testando isso aqui".encode("utf-8")
                ),
                "type": "text/plain",
            }
        ]

    def __test_creation(self) -> None:
        attachment_creation_service: IService[None] = AttachmentCreationService(
            self.__occurrence_payload, *self.__attachment_payload.attachments
        )

        attachment_creation_service.execute()

    def test_getting(self) -> None:
        attachment_getting_service: IService[
            Mapping[str, Any]
        ] = AttachmentGettingService(self.__attachment_payload.id_uuid)

        attachment_data: Mapping[str, Any] = attachment_getting_service.execute()

        pprint(f"=============> {attachment_data}")

        self.assertTrue(attachment_data)
