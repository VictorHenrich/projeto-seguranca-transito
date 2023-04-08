from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime

from ..util import TestUtil

TestUtil.load_modules()

import src.start.application
from src.patterns.service import IService
from src.models import User
from src.services.user import (
    UserCreationService,
    UserCreationServiceProps,
    UserUpdateService,
    UserUpdateServiceProps,
    UserExclusionService,
    UserExclusionServiceProps,
    UserFindingService,
    UserFindingServiceProps,
    UserAuthenticationService,
    UserAuthenticationServiceProps,
)


class TestUserService(TestCase):
    def test_creation_user(self) -> None:
        user_creation_props: Mock = Mock()

        user_creation_props.name = "Usuário teste"
        user_creation_props.email = "tarso@gmail.com"
        user_creation_props.password = "1234"
        user_creation_props.document = "1111111"
        user_creation_props.birthday = None

        user_creation_service: IService[
            UserCreationServiceProps, None
        ] = UserCreationService()

        user_creation_service.execute(user_creation_props)

    def test_update_user(self) -> None:
        user_update_props: Mock = Mock()

        user_update_props.user_uuid = "1253fc3f-6d1d-4ce3-a009-ac91e24c3a91"
        user_update_props.name = "Usuário Alterado"
        user_update_props.email = "teste@gmail.com"
        user_update_props.password = "1234"
        user_update_props.document = "1111111"
        user_update_props.birthday = datetime.now().date()
        user_update_props.status = False

        user_update_service: IService[
            UserUpdateServiceProps, None
        ] = UserUpdateService()

        user_update_service.execute(user_update_props)

    def test_exclusion_user(self) -> None:
        user_exclusion_props: Mock = Mock()

        user_exclusion_props.user_uuid = "1253fc3f-6d1d-4ce3-a009-ac91e24c3a91"

        user_exclusion_service: IService[
            UserExclusionServiceProps, None
        ] = UserExclusionService()

        user_exclusion_service.execute(user_exclusion_props)

    def test_finding_user(self) -> None:
        user_finding_props: Mock = Mock()

        user_finding_props.user_uuid = "8520b889-c1ef-4ae7-9651-6d5bc9672748"

        user_finding_service: IService[
            UserFindingServiceProps, User
        ] = UserFindingService()

        user: User = user_finding_service.execute(user_finding_props)

        self.assertTrue(user)

    def test_auth_user(self) -> None:
        user_auth_props: Mock = Mock()

        user_auth_props.email = "stephaniemachadow@gmail.com"
        user_auth_props.password = "1234"

        user_auth_service: IService[
            UserAuthenticationServiceProps, str
        ] = UserAuthenticationService()

        token: str = user_auth_service.execute(user_auth_props)

        self.assertTrue(token)
