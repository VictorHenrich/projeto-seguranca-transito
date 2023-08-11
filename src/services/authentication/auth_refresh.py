from models import User
from patterns.service import IService
from .auth_verification import AuthVerificationService
from .authentication import AuthenticationService


class AuthRefreshService:
    def __init__(self, token: str) -> None:
        self.__token: str = token

    def __verify_token(self) -> User:
        verify_user_auth_service: IService[User] = AuthVerificationService(self.__token)

        return verify_user_auth_service.execute()

    def __authenticate_user(self, user: User) -> str:
        user_authenticate_service: IService[str] = AuthenticationService(
            user.email, user.senha
        )

        return user_authenticate_service.execute()

    def execute(self) -> str:
        user: User = self.__verify_token()

        return self.__authenticate_user(user)
