from unittest import TestCase
from unittest.mock import Mock
from datetime import datetime

from ..util import TestUtil

TestUtil.load_modules()

import src.main
from src.patterns.service import IService
from src.models import User
from src.services.user import (
    UserCreationService,
    UserUpdateService,
    UserExclusionService,
    UserFindingService,
    UserAuthenticationService,
)


class TestUserService(TestCase):
    def test_creation_user(self) -> None:
        user_creation_props: Mock = Mock()

        user_creation_props.name = "Usuário teste"
        user_creation_props.email = "tarso@gmail.com"
        user_creation_props.password = "1234"
        user_creation_props.document = "1111111"
        user_creation_props.birthday = None

        user_creation_service: IService[None] = UserCreationService(
            name=user_creation_props.name,
            email=user_creation_props.email,
            password=user_creation_props.oassword,
            document=user_creation_props.document,
            birthday=user_creation_props.birthday,
        )

        user_creation_service.execute()

    def test_update_user(self) -> None:
        user_update_props: Mock = Mock()

        user_update_props.user_uuid = "1253fc3f-6d1d-4ce3-a009-ac91e24c3a91"
        user_update_props.name = "Usuário Alterado"
        user_update_props.email = "teste@gmail.com"
        user_update_props.password = "1234"
        user_update_props.document = "1111111"
        user_update_props.birthday = datetime.now().date()
        user_update_props.status = False

        user_update_service: IService[None] = UserUpdateService(
            user_uuid=user_update_props.user_uuid,
            name=user_update_props.name,
            email=user_update_props.email,
            password=user_update_props.password,
            document=user_update_props.document,
            birthday=user_update_props.birthday,
            status=user_update_props.status,
        )

        user_update_service.execute()

    def test_exclusion_user(self) -> None:
        user_exclusion_props: Mock = Mock()

        user_exclusion_props.user_uuid = "1253fc3f-6d1d-4ce3-a009-ac91e24c3a91"

        user_exclusion_service: IService[None] = UserExclusionService(
            user_uuid=user_exclusion_props.user_uuid
        )

        user_exclusion_service.execute()

    def test_finding_user(self) -> None:
        user_finding_props: Mock = Mock()

        user_finding_props.user_uuid = "8520b889-c1ef-4ae7-9651-6d5bc9672748"

        user_finding_service: IService[User] = UserFindingService(
            user_uuid=user_finding_props.user_uuid
        )

        user: User = user_finding_service.execute()

        self.assertTrue(user)

    def test_auth_user(self) -> None:
        user_auth_props: Mock = Mock()

        user_auth_props.email = "stephaniemachadow@gmail.com"
        user_auth_props.password = "1234"

        user_auth_service: IService[str] = UserAuthenticationService(
            email=user_auth_props.email, password=user_auth_props.password
        )

        token: str = user_auth_service.execute()

        self.assertTrue(token)
