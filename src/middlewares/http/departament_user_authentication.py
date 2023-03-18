from flask import request
from typing import Optional
from datetime import datetime

from server.http import Middleware, ResponseInauthorized
from server.utils import UtilsJWT, UtilsExcept
from models import Agent, Departament
from patterns.service import IService
from services.agent import AgentGettingService
from services.departament import DepartamentGettingUUIDService
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
    DepartamentNotFoundError,
)
from utils.entities import PayloadDepartamentUserJWT
from start import app


class DepartamentUserAuthenticationMiddleware(Middleware):
    @classmethod
    def handle(cls):
        token: Optional[str] = request.headers.get("Authorization")

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

        departament_service: IService[Departament] = DepartamentGettingUUIDService()

        departament_user_service: IService[Agent] = AgentGettingService()

        departament: Departament = departament_service.execute(
            uuid_departament=payload.uuid_departament
        )

        departament_user: Agent = departament_user_service.execute(
            uuid_departament_user=payload.uuid_user, departament=departament
        )

        return {"auth_user": departament_user, "auth_departament": departament}

    @classmethod
    def catch(cls, exception: Exception):
        validation: bool = UtilsExcept.fired(
            exception,
            DepartamentNotFoundError,
            DepartamentNotFoundError,
            UserNotFoundError,
            ExpiredTokenError,
            AuthorizationNotFoundHeader,
        )

        if validation:
            return ResponseInauthorized(data=str(exception))

        raise exception
