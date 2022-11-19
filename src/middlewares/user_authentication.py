from flask import request
from typing import Optional
from datetime import datetime

from server.http import Middleware, ResponseInauthorized
from server.database import Database
from server.utils import UtilsJWT
from models import Usuario
from patterns import InterfaceService
from services.user import UserLoadingService
from services.user.entities import UserLocation
from exceptions import (
    AuthorizationNotFoundHeader, 
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError
)
from utils.entities import PayloadUserJWT
from start import app



class UserAuthenticationMiddleware(Middleware):
    @classmethod
    def handle(cls):
        token: Optional[str] = request.headers.get('Authorization')

        if not token:
            raise AuthorizationNotFoundHeader()

        if 'Bearer' not in token:
            raise TokenTypeNotBearerError()

        token = token.replace('Bearer ', '')

        payload: PayloadUserJWT = \
            UtilsJWT.decode(token, app.http.configs.secret_key, PayloadUserJWT)

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        location_data: UserLocation = UserLocation(payload.expired)

        service: InterfaceService[UserLocation] = UserLoadingService()

        user: service.execute(location_data)

        return {"auth": user}

    @classmethod
    def catch(cls, exception: Exception):
        exceptions: list[Exception] = [
            ExpiredTokenError,
            UserNotFoundError,
            TokenTypeNotBearerError
        ]

        if type(exception) in exceptions:
            return ResponseInauthorized(data=str(exception))

        raise exception
        