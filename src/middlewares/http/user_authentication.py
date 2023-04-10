from server import App
from server.http import HttpMiddleware, ResponseInauthorized
from patterns.service import IService
from models import User
from services.user import VerifyUserAuthService, VerifyUserAuthServiceProps
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
)


class UserAuthenticationMiddleware(HttpMiddleware[None]):
    def handle(self, props: None):
        token: str = App.http.global_request.headers.get("Authorization") or ""

        verify_user_auth_props: VerifyUserAuthServiceProps = VerifyUserAuthServiceProps(
            token
        )

        verify_user_auth_service: IService[
            VerifyUserAuthServiceProps, User
        ] = VerifyUserAuthService()

        user = verify_user_auth_service.execute(verify_user_auth_props)

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
