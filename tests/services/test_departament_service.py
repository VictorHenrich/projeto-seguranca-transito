from unittest import TestCase
from unittest.mock import Mock

from ..util import TestUtil

TestUtil.load_modules()

import src.start.application
from src.patterns.service import IService
from src.models import Departament
from src.services.departament import (
    DepartamentCreationService,
    DepartamentCreationServiceProps,
    DepartamentFindingService,
    DepartamentFindingServiceProps,
    DepartamentFindingUUIDService,
    DepartamentFindingUUIDServiceProps,
)


class TestDepartamentService(TestCase):
    def test_creation_departament(self) -> None:
        departament_creation_props: Mock = Mock()

        departament_creation_props.name = "TESTE"
        departament_creation_props.unit = "teste-81"
        departament_creation_props.access = "teste"
        departament_creation_props.zipcode = "11111"
        departament_creation_props.state = "RS"
        departament_creation_props.city = "Porto Alegre"
        departament_creation_props.district = "Bairro teste"
        departament_creation_props.street = "Rua teste"
        departament_creation_props.complement = ""

        departament_creation_service: IService[
            DepartamentCreationServiceProps, None
        ] = DepartamentCreationService()

        departament_creation_service.execute(departament_creation_props)

    def test_finding_departament(self) -> None:
        departament_finding_props: Mock = Mock()

        departament_finding_props.departament_id = 3

        departament_finding_service: IService[
            DepartamentFindingServiceProps, Departament
        ] = DepartamentFindingService()

        departament: Departament = departament_finding_service.execute(
            departament_finding_props
        )

        self.assertTrue(departament)

    def test_finding_uuid_departament(self) -> None:
        departament_finding_props: Mock = Mock()

        departament_finding_props.departament_uuid = (
            "efd0f1c8-4f32-4f3c-b7c2-1f73fa37f891"
        )

        departament_finding_service: IService[
            DepartamentFindingUUIDServiceProps, Departament
        ] = DepartamentFindingUUIDService()

        departament: Departament = departament_finding_service.execute(
            departament_finding_props
        )

        self.assertTrue(departament)
