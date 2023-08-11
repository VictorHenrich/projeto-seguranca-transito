from unittest import TestCase
from unittest.mock import Mock
from pprint import pprint
from datetime import datetime

from .database import database
from src.models import User
from src.patterns.repository import (
    IAuthRepository,
    ICreateRepository,
    IUpdateRepository,
    IFindRepository,
)
from src.repositories.user import (
    UserAuthRepository,
    UserAuthRepositoryParams,
    UserCreateRepository,
    UserCreateRepositoryParams,
    UserFindAndUpdateRepository,
    UserFindAndUpdateRepositoryParams,
    UserFindRepository,
    UserFindRepositoryParams,
)


class UserRepositoryCase(TestCase):
    def setUp(self) -> None:
        self.__user_payload: Mock = Mock()

        self.__user_payload.email = "pessoinha123@gmail.com"
        self.__user_payload.password = "1234"
        self.__user_payload.user_uuid = ""
        self.__user_payload.name = "Fulano"
        self.__user_payload.document = "22222222222"
        self.__user_payload.document_rg = "111111"
        self.__user_payload.telephone = "1111111"
        self.__user_payload.state_issuer = "SANTA CATARINA"
        self.__user_payload.address_state = "SC"
        self.__user_payload.address_city = "CIDADE TAL"
        self.__user_payload.address_district = "BAIRRO TAL"
        self.__user_payload.address_street = "RUA TAL"
        self.__user_payload.address_number = "S/N"
        self.__user_payload.birthday = datetime.now().date()

    def test_create(self) -> None:
        with database.create_session() as session:
            user_repository: ICreateRepository[
                UserCreateRepositoryParams, User
            ] = UserCreateRepository(session)

            user_created: User = user_repository.create(self.__user_payload)

            pprint(f"USER CREATED ===> {user_created}")

            self.assertTrue(user_created)

    def test_auth(self) -> None:
        with database.create_session() as session:
            user_repository: IAuthRepository[
                UserAuthRepositoryParams, User
            ] = UserAuthRepository(session)

            user: User = user_repository.auth(self.__user_payload)

            pprint(f"USER AUTHORIZED ======> {user}")

            self.assertTrue(user)

    def test_find(self) -> None:
        with database.create_session() as session:
            user_repository: IFindRepository[
                UserFindRepositoryParams, User
            ] = UserFindRepository(session)

            user_finded: User = user_repository.find_one(self.__user_payload)

            pprint(f"USER FINDED ===> {user_finded}")

            self.assertTrue(user_finded)

    def test_update(self) -> None:
        with database.create_session() as session:
            user_repository: IUpdateRepository[
                UserFindAndUpdateRepositoryParams, User
            ] = UserFindAndUpdateRepository(session)

            user_updated: User = user_repository.update(self.__user_payload)

            pprint(f"USER UPDATED ===> {user_updated}")

            self.assertTrue(user_updated)
