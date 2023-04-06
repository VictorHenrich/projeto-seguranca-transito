from typing import Optional
from datetime import date, datetime
from unittest import TestCase
from unittest.mock import Mock
from dataclasses import dataclass

from src.server import App
from src.models.user import User
from src.patterns.repository.iauth_repository import IAuthRepository
from src.repositories.user import UserAuthRepository, UserAuthRepositoryParam
from src.repositories.user import UserCreateRepository, UserCreateRepositoryParams
from src.repositories.user import UserUpdateRepository, UserUpdateRepositoryParam


@dataclass
class UserCreateParams:
    name: str
    email: str
    password: str
    document: str
    birthday: Optional[date]


@dataclass
class UserUpdateParams:
    uuid_user: str
    name: str
    email: str
    password: str
    document: str
    birthday: date
    status: bool


class TestUserRepository(TestCase):
    def test_create_user(self):
        user_create_params: UserCreateRepositoryParams = UserCreateParams(
            "victor",
            "VICTORHENRICH993@GMAIL.COM",
            "1234",
            "02988790000",
            datetime.now().date(),
        )

        with App.databases.create_session() as session:
            user_create_repository: UserCreateRepository = UserCreateRepository(session)

            user_create_repository.create(user_create_params)

            session.commit()

    def test_user_auth(self):
        user_auth_params: Mock = Mock()

        user_auth_params.email.return_value = "victorhenrich993@gmail.com"
        user_auth_params.password.return_value = "1234"

        with App.databases.create_session() as session:
            user_auth_repository: IAuthRepository[
                UserAuthRepositoryParam, User
            ] = UserAuthRepository(session)

            user: User = user_auth_repository.auth(user_auth_params)

            self.assertIsNotNone(user)

    def test_user_update(self):
        user_update_params: UserUpdateRepositoryParam = UserUpdateParams(
            "",
            "victor",
            "VICTORHENRICH993@GMAIL.COM",
            "1234",
            "02988790000",
            datetime.now().date(),
            True,
        )

        with App.databases.create_session() as session:
            user_update_repository: UserUpdateRepository = UserUpdateRepository(session)

            user_update_repository.update(user_update_params)
