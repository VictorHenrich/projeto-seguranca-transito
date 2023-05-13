from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime

from ..util import TestUtil

TestUtil.load_modules()

import src.main
from src.patterns.service import IService
from src.services.integrations import OccurrenceIntegrationCreationService


class TestOccurrenceIntegration(TestCase):
    def test_create_occurrence(self) -> None:
        user_payload: Mock = Mock()
        occurrence_payload: Mock = Mock()
        vehicle_payload: Mock = Mock()

        user_payload.email = "victorhenrich993@gmail.com"
        user_payload.nome = "victor henrich"
        user_payload.data_nascimento = datetime(1998, 5, 27).date()
        user_payload.cpf = "02988790000"
        user_payload.rg = "11111111111"
        user_payload.estado_emissor = "SANTA CATARINA"
        user_payload.endereco_uf = "SC"
        user_payload.endereco_bairro = "caçador"
        user_payload.endereco_logradouro = "Antonio Manuel dos Santos"
        user_payload.endereco_numero = "393"
        user_payload.endereco_cidade = "capivari de baixo"
        user_payload.telefone = "048999187582"

        occurrence_payload.data_cadastro = datetime.now()
        occurrence_payload.endereco_cidade = "capivari de baixo"
        occurrence_payload.endereco_bairro = "caçador"
        occurrence_payload.endereco_logragouro = "rua antônio manuel dos santos"
        occurrence_payload.endereco_numero = "393"
        occurrence_payload.endereco_uf = "SC"
        occurrence_payload.obs = """
                Eu estava andando de boa quando do nada o carro veio
                e se xocou contra meu carro, fazendo eu derrapar e bater em uma parade,
                já consegui pegar informações da outra pessoa, tal tal ta tal
            """

        vehicle_payload.placa = "111111111"
        vehicle_payload.renavam = "11111111"
        vehicle_payload.tipo_veiculo = "carro"
        vehicle_payload.marca = None
        vehicle_payload.modelo = None
        vehicle_payload.cor = None
        vehicle_payload.ano = None
        vehicle_payload.chassi = None
        vehicle_payload.possui_seguro = False

        service: IService[None] = OccurrenceIntegrationCreationService(
            occurrence=occurrence_payload, user=user_payload, vehicle=vehicle_payload
        )

        service.execute()
