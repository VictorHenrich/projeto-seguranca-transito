from typing import Optional
from datetime import datetime

from start import app
from server.websocket import Middleware
from server.utils import UtilsJWT
from models import UsuarioDepartamento, Departamento
from patterns.service import IService
from services.departament_user import DepartamentUserGettingService
from services.departament import DepartamentGettingUUIDService
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError
)
from utils.entities import PayloadDepartamentUserJWT
from start import app


class DepartamentUserAuthenticationMiddleware(Middleware):
    @classmethod
    def handle(cls):
        token: Optional[str] = app.websocket.global_request.headers.get("Authorization")

        if not token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in token:
            raise TokenTypeNotBearerError()

        token = token.replace("Bearer ", "")

        payload: PayloadDepartamentUserJWT = UtilsJWT.decode(
            token, app.http.configs.secret_key, PayloadDepartamentUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        departament_service: IService[Departamento] = DepartamentGettingUUIDService()

        departament_user_service: IService[
            UsuarioDepartamento
        ] = DepartamentUserGettingService()

        departament: Departamento = departament_service.execute(
            uuid_departament=payload.uuid_departament
        )

        departament_user: UsuarioDepartamento = departament_user_service.execute(
            uuid_departament_user=payload.uuid_user, departament=departament
        )

        return {"auth_user": departament_user, "auth_departament": departament}
