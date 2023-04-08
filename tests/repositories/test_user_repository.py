from unittest import TestCase
from unittest.mock import Mock

from ..util import TestUtil

TestUtil.load_modules()

from src.start.application import App
from src.models import User
from src.patterns.repository import (
    IAuthRepository,
    ICreateRepository,
    IUpdateRepository,
    IDeleteRepository,
    IFindRepository,
)
from src.repositories.user import (
    UserAuthRepository,
    UserAuthRepositoryParams,
    UserCreateRepository,
    UserCreateRepositoryParams,
    UserUpdateRepository,
    UserUpdateRepositoryParams,
    UserDeleteRepository,
    UserDeleteRepositoryParams,
    UserFindRepository,
    UserFindRepositoryParams,
)


class TestUserRepository(TestCase):
    def test_user_auth(self) -> None:
        user_auth_params: Mock = Mock()

        user_auth_params.email = "victorhenrich993@gmail.com"
        user_auth_params.password = "1234"

        with App.databases.create_session() as session:
            user_auth_repository: IAuthRepository[
                UserAuthRepositoryParams, User
            ] = UserAuthRepository(session)

            user: User = user_auth_repository.auth(user_auth_params)

            self.assertTrue(user)

    def test_create_user(self) -> None:
        user_create_params: Mock = Mock()

        user_create_params.name = "Stephanie Machado"
        user_create_params.email = "stephaniemachadow@gmail.com"
        user_create_params.password = "1234"
        user_create_params.document = "09867514998"
        user_create_params.birthday = None

        with App.databases.create_session() as session:
            user_create_repository: ICreateRepository[
                UserCreateRepositoryParams, None
            ] = UserCreateRepository(session)

            user_create_repository.create(user_create_params)

            session.commit()

    def test_update_user(self) -> None:
        user_update_params: Mock = Mock()

        user_update_params.user_uuid = "8a3f3346-d0c7-4b8a-ab8c-408999335872"
        user_update_params.name = "Nome alterado"
        user_update_params.email = "victorhenrich@hotmail.com"
        user_update_params.password = "1234"
        user_update_params.document = "02888790000"
        user_update_params.birthday = None
        user_update_params.status = True

        with App.databases.create_session() as session:
            user_update_repository: IUpdateRepository[
                UserUpdateRepositoryParams, None
            ] = UserUpdateRepository(session)

            user_update_repository.update(user_update_params)

            session.commit()

    def test_delete_user(self) -> None:
        user_delete_params: Mock = Mock()

        user_delete_params.user_uuid = "8a3f3346-d0c7-4b8a-ab8c-408999335872"

        with App.databases.create_session() as session:
            user_delete_repository: IDeleteRepository[
                UserDeleteRepositoryParams, None
            ] = UserDeleteRepository(session)

            user_delete_repository.delete(user_delete_params)

            session.commit()

    def test_find_user(self) -> None:
        user_find_params: Mock = Mock()

        user_find_params.user_uuid = "8520b889-c1ef-4ae7-9651-6d5bc9672748"

        with App.databases.create_session() as session:
            user_find_repository: IFindRepository[
                UserFindRepositoryParams, User
            ] = UserFindRepository(session)

            user: User = user_find_repository.find_one(user_find_params)

            self.assertIsNotNone(user)
