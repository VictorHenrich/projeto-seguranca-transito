from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime

from ..util import TestUtil

TestUtil.load_modules()

import src.main
from src.patterns.service import IService
from src.services.webdriver.occurrence_integration import OccurrenceIntegrationService


class TestOccurrenceIntegration(TestCase):
    def test_web_driver(self) -> None:
        user_payload: Mock = Mock()

        occurrence_payload: Mock = Mock()

        user_payload.email = "victorhenrich993@gmail.com"
        user_payload.nome = "victor henrich"
        user_payload.data_nascimento = datetime(1998, 5, 27).date()
        user_payload.cpf = "02988790000"
        user_payload.rg = "11111111111"
        user_payload.estado_emissor = "SANTA CATARINA"

        occurrence_payload.occurrence_date = datetime.now()
        occurrence_payload.city = "capivari de baixo"
        occurrence_payload.district = "caçador"
        occurrence_payload.street = "rua antônio manuel dos santos"

        service: IService[None] = OccurrenceIntegrationService(
            occurrence_date=occurrence_payload.occurrence_date,
            city=occurrence_payload.city,
            district=occurrence_payload.district,
            street=occurrence_payload.street,
            user=user_payload,
        )

        service.execute()
