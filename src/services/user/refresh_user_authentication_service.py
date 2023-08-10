from models import User
from patterns.service import IService
from .verify_user_auth_service import VerifyUserAuthService
from .user_authentication_service import UserAuthenticationService


class RefreshUserAuthenticationService:
    def __init__(self, token: str) -> None:
        self.__token: str = token

    def __verify_token(self) -> User:
        verify_user_auth_service: IService[User] = VerifyUserAuthService(self.__token)

        return verify_user_auth_service.execute()

    def __authenticate_user(self, user: User) -> str:
        user_authenticate_service: IService[str] = UserAuthenticationService(
            user.email, user.senha
        )

        return user_authenticate_service.execute()

    def execute(self) -> str:
        user: User = self.__verify_token()

        return self.__authenticate_user(user)
