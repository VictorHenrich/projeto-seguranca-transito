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
        user_payload.end_uf = "SC"
        user_payload.end_bairro = "caçador"
        user_payload.end_logradouro = "Antonio Manuel dos Santos"
        user_payload.end_numero = "393"

        occurrence_payload.data_cadastro = datetime.now()
        occurrence_payload.endereco_cidade = "capivari de baixo"
        occurrence_payload.endereco_bairro = "caçador"
        occurrence_payload.endereco_logradouro = "rua antônio manuel dos santos"
        occurrence_payload.endereco_numero = "393"

        service: IService[None] = OccurrenceIntegrationService(
            occurrence=occurrence_payload,
            user=user_payload,
        )

        service.execute()
