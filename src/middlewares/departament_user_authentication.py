from flask import request
from typing import Optional
from datetime import datetime

from server.http import Middleware, ResponseInauthorized
from server.database import Database
from server.utils import UtilsJWT
from models import UsuarioDepartamento, Departamento
from services.departament_user import DepartamentUserLoadingService
from services.departament import DepartamentLoadingService
from services.departament_user.entities import DepartamentUserLocation
from services.departament.entities import DepartamentLocation
from exceptions import (
    AuthorizationNotFoundHeader, 
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
    DepartamentNotFoundError
)
from patterns import InterfaceService
from utils.entities import PayloadDepartamentUserJWT
from start import app



db: Database = app.databases.get_database()





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

        param_departament: DepartamentLocation = DepartamentLocation(payload.uuid_departament)
        service_departament: InterfaceService[DepartamentLocation] = DepartamentLoadingService()

        departament: Departamento = service_departament.execute(param_departament)

        param_departament_user: DepartamentUserLocation = DepartamentUserLocation(payload.uuid_user, departament)
        service_departament_user: InterfaceService[DepartamentUserLocation] = DepartamentUserLoadingService()

        user: UsuarioDepartamento = service_departament_user.execute(param_departament_user)

        return {"auth_user": user, "auth_departament": departament}


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


        