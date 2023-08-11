from unittest import TestCase
from unittest.mock import Mock
import logging


from src.patterns.service import IService
from src.models import User
from src.services.authentication import (
    AuthenticationService,
    AuthRefreshService,
    AuthVerificationService,
)


class AuthenticationServiceCase(TestCase):
    def setUp(self) -> None:
        self.__user: Mock = Mock()

        self.__user.email = "victorhenrich993@gmail.com"
        self.__user.password = "1234"

        self.__user_auth: str = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX3V1aWQiOiJmM2UxODRkYS04ZDYxLTQzMGItYjAyNS0xMmE4MzA4NGFjY2IiLCJleHBpcmVkIjoxNjkxNzg1MzU1LjIwOTg2Nn0.37Jz1o05xvgbs92wvgE4LMtPCklKTAsV9QVXnXQw914"

    def test_authentication(self) -> None:
        auth_service: IService[str] = AuthenticationService(
            self.__user.email, self.__user.password
        )

        token: str = auth_service.execute()

        logging.info(f"Token Gerado: {token}")

        self.assertTrue(token)

    def test_verify_token(self) -> None:
        auth_verification_service: IService[User] = AuthVerificationService(
            self.__user_auth
        )

        user_located: User = auth_verification_service.execute()

        logging.info(f"Usuário localizado: {user_located}")

        self.assertTrue(user_located)

    def test_refresh_token(self) -> None:
        auth_refresh_service: IService[str] = AuthRefreshService(self.__user_auth)

        token_refreshed: str = auth_refresh_service.execute()

        logging.info(f"Token Regerado: {token_refreshed}")

        self.assertTrue(token_refreshed)
