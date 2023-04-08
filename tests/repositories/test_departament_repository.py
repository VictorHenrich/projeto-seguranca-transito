from unittest import TestCase
from unittest.mock import Mock

from ..util import TestUtil

TestUtil.load_modules()


from src.start.application import App
from src.models import Departament
from src.patterns.repository import ICreateRepository, IFindRepository
from src.repositories.departament import (
    DepartamentCreateRepository,
    DepartamentCreateRepositoryParams,
    DepartamentFindRepository,
    DepartamentFindRepositoryParams,
    DepartamentFindUUIDRepository,
    DepartamentFindUUIDRepositoryParams,
)


class TestDepartamentRepository(TestCase):
    def test_create_departament(self) -> None:
        departament_create_params: Mock = Mock()

        departament_create_params.name = "Departamento de teste"
        departament_create_params.unit = "Unidade 2"
        departament_create_params.access = "UN2"
        departament_create_params.zipcode = "00001"
        departament_create_params.state = "SC"
        departament_create_params.city = "Tubarão"
        departament_create_params.district = "Bairro não sei das quantas"
        departament_create_params.street = "Rua tal"
        departament_create_params.complement = ""

        with App.databases.create_session() as session:
            departament_create_repository: ICreateRepository[
                DepartamentCreateRepositoryParams, None
            ] = DepartamentCreateRepository(session)

            departament_create_repository.create(departament_create_params)

            session.commit()

    def test_find_departament(self) -> None:
        departament_find_params: Mock = Mock()

        departament_find_params.departament_id = 1

        with App.databases.create_session() as session:
            departament_find_repository: IFindRepository[
                DepartamentFindRepositoryParams, Departament
            ] = DepartamentFindRepository(session)

            departament: Departament = departament_find_repository.find_one(
                departament_find_params
            )

            self.assertTrue(departament)

    def test_find_uuid_departament(self) -> None:
        departament_find_params: Mock = Mock()

        departament_find_params.departament_uuid = (
            "07b9c089-4f16-4075-8710-f7173f710d4b"
        )

        with App.databases.create_session() as session:
            departament_find_repository: IFindRepository[
                DepartamentFindUUIDRepositoryParams, Departament
            ] = DepartamentFindUUIDRepository(session)

            departament: Departament = departament_find_repository.find_one(
                departament_find_params
            )

            self.assertTrue(departament)
