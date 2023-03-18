from flask import request
from typing import Optional
from datetime import datetime

from server.websocket import Middleware
from server.utils import UtilsJWT
from patterns.service import IService
from models import User
from services.user import UserGettingService, UserGettingServiceProps
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
)
from utils.entities import PayloadUserJWT
from start import app


class UserAuthenticationMiddleware(Middleware):
    @classmethod
    def handle(cls):
        token: Optional[str] = app.websocket.global_request.headers.get("Authorization")

        if not token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in token:
            raise TokenTypeNotBearerError()

        token = token.replace("Bearer ", "")

        payload: PayloadUserJWT = UtilsJWT.decode(
            token, app.http.configs.secret_key, PayloadUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        service: IService[UserGettingServiceProps, User] = UserGettingService()

        service_props: UserGettingServiceProps = UserGettingServiceProps(
            uuid_user=payload.uuid_user
        )

        user: User = service.execute(service_props)

        return {"auth": user}
