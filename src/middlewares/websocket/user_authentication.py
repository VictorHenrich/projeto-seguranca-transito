from flask import request
from typing import Optional, Dict
from datetime import datetime

from server.websocket import SocketMiddleware
from server.utils import UtilsJWT
from patterns.service import IService
from models import User
from services.user import UserFindingService, UserFindingServiceProps
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
)
from utils.entities import PayloadUserJWT
from server import App


class UserAuthenticationMiddleware(SocketMiddleware[None]):
    def handle(self, props: None) -> Dict[str, User]:
        token: Optional[str] = App.websocket.global_request.headers.get("Authorization")

        if not token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in token:
            raise TokenTypeNotBearerError()

        token = token.replace("Bearer ", "")

        payload: PayloadUserJWT = UtilsJWT.decode(
            token, App.http.configs.secret_key, PayloadUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        service: IService[UserFindingServiceProps, User] = UserFindingService()

        service_props: UserFindingServiceProps = UserFindingServiceProps(
            user_uuid=payload.user_uuid
        )

        user: User = service.execute(service_props)

        return {"auth": user}
