from flask import request
from typing import Optional
from datetime import datetime

from server.http import Middleware, ResponseInauthorized
from server.utils import UtilsJWT
from models import UsuarioDepartamento, Departamento
from patterns.service import IService
from services.departament_user import DepartamentUserGettingService
from services.departament import DepartamentGettingUUIDService
from exceptions import (
    AuthorizationNotFoundHeader, 
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
    DepartamentNotFoundError
)
from utils.entities import PayloadDepartamentUserJWT
from start import app





class DepartamentUserAuthenticationMiddleware(Middleware):
    @classmethod
    def handle(cls):
        token: Optional[str] = request.headers.get('Authorization')

        if not token:
            raise AuthorizationNotFoundHeader()

        if 'Bearer' not in token:
            raise TokenTypeNotBearerError()

        token = token.replace('Bearer ', '')

        payload: PayloadDepartamentUserJWT = \
            UtilsJWT.decode(token, app.http.configs.secret_key, PayloadDepartamentUserJWT)

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        departament_service: IService[Departamento] = \
            DepartamentGettingUUIDService()

        departament_user_service: IService[UsuarioDepartamento] = \
            DepartamentUserGettingService()

        departament: Departamento = \
            departament_service.execute(
                uuid_departament=payload.uuid_departament
            )

        departament_user: UsuarioDepartamento = \
            departament_user_service.execute(
                uuid_departament_user=payload.uuid_user,
                departament=departament
            )

        return {"auth_user": departament_user, "auth_departament": departament}


    @classmethod
    def catch(cls, exception: Exception):
        exceptions: list[Exception] = [
            DepartamentNotFoundError,
            DepartamentNotFoundError,
            UserNotFoundError,
            ExpiredTokenError
        ]

        if type(exception) in exceptions:
            return ResponseInauthorized(data=str(exception))

        raise exception


        