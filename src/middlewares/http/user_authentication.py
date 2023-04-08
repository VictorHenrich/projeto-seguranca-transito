from flask import request
from typing import Optional
from datetime import datetime

from server.http import HttpMiddleware, ResponseInauthorized
from server.utils import UtilsJWT
from patterns.service import IService
from models import User
from services.user import UserFindingService, UserFindingServiceProps
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
)
from utils.entities import PayloadUserJWT
from server import App


class UserAuthenticationMiddleware(HttpMiddleware[None]):
    def handle(self, props: None):
        token: Optional[str] = request.headers.get("Authorization")

        if not token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in token:
            raise TokenTypeNotBearerError()

        token = token.replace("Bearer ", "")

        payload: PayloadUserJWT = UtilsJWT.decode(
            token, App.http.configs.secret_key, class_=PayloadUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        service: IService[UserFindingServiceProps, User] = UserFindingService()

        service_props: UserFindingServiceProps = UserFindingServiceProps(
            user_uuid=payload.user_uuid
        )

        user: User = service.execute(service_props)

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
