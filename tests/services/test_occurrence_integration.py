from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime

from ..util import TestUtil

TestUtil.load_modules()

import src.main
from src.patterns.service import IService
from src.services.webdriver import OccurrenceIntegrationService


class TestOccurrenceIntegration(TestCase):
    def test_web_driver(self) -> None:
        webdriver_payload: Mock = Mock()

        webdriver_payload.occurrence_date = datetime.now()
        webdriver_payload.city = "capivari de baixo"
        webdriver_payload.district = "caçador"
        webdriver_payload.street = "rua antônio manuel dos santos"

        service: IService[None] = OccurrenceIntegrationService(
            occurrence_date=webdriver_payload.occurrence_date,
            city=webdriver_payload.city,
            district=webdriver_payload.district,
            street=webdriver_payload.district
        )

        service.execute()
