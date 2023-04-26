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
        webdriver_payload.city = "CAPIVARI DE BAIXO"
        webdriver_payload.district = "CAÇADOR"
        webdriver_payload.street = "RUA ANTONIO MANUEL DOS SANTOS"

        service: IService[None] = OccurrenceIntegrationService(
            occurrence_date=webdriver_payload.occurrence_date,
            city=webdriver_payload.city,
            district=webdriver_payload.district,
            street=webdriver_payload.district
        )

        service.execute()
