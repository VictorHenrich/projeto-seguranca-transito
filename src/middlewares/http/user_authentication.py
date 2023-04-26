from server import App
from server.http import HttpMiddleware, ResponseInauthorized
from patterns.service import IService
from models import User
from services.user import VerifyUserAuthService
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
)


class UserAuthenticationMiddleware(HttpMiddleware[None]):
    def handle(self, props: None):
        token: str = App.http.global_request.headers.get("Authorization") or ""

        verify_user_auth_service: IService[User] = VerifyUserAuthService(token)

        user: User = verify_user_auth_service.execute()

        return {"auth": user}

    def catch(self, exception: Exception):
        validation: bool = isinstance(
            exception,
            (
                ExpiredTokenError,
                UserNotFoundError,
                TokenTypeNotBearerError,
                AuthorizationNotFoundHeader,
            ),
        )

        if validation:
            return ResponseInauthorized(data=str(exception))

        raise exception
