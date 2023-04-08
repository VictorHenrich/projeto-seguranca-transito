from unittest import TestCase
from unittest.mock import Mock

from ..util import TestUtil

TestUtil.load_modules()

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

        departament_creation_props.name = ""
        departament_creation_props.unit = ""
        departament_creation_props.access = ""
        departament_creation_props.zipcode = ""
        departament_creation_props.state = ""
        departament_creation_props.city = ""
        departament_creation_props.district = ""
        departament_creation_props.street = ""
        departament_creation_props.complement = ""

        departament_creation_service: IService[
            DepartamentCreationServiceProps, None
        ] = DepartamentCreationService()

        departament_creation_service.execute(departament_creation_props)

    def test_finding_departament(self) -> None:
        departament_finding_props: Mock = Mock()

        departament_finding_props.departament_id = 1

        departament_finding_service: IService[
            DepartamentFindingServiceProps, Departament
        ] = DepartamentFindingService()

        departament: Departament = departament_finding_service.execute(
            departament_finding_props
        )

        self.assertTrue(departament)

    def test_finding_uuid_departament(self) -> None:
        departament_finding_props: Mock = Mock()

        departament_finding_props.departament_uuid = ""

        departament_finding_service: IService[
            DepartamentFindingUUIDServiceProps, Departament
        ] = DepartamentFindingUUIDService()

        departament: Departament = departament_finding_service.execute(
            departament_finding_props
        )

        self.assertTrue(departament)
