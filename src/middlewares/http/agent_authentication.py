from flask import request
from typing import Optional
from datetime import datetime

from server.http import HttpMiddleware, ResponseInauthorized
from server.utils import UtilsJWT
from models import Agent, Departament
from patterns.service import IService
from services.agent import AgentFindingService, AgentFindingServiceProps
from services.departament import (
    DepartamentFindingUUIDService,
    DepartamentFindingUUIDServiceProps,
)
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
    DepartamentNotFoundError,
)
from utils.entities import PayloadDepartamentUserJWT
from server import App


class AgentAuthenticationMiddleware(HttpMiddleware[None]):
    def handle(self, props: None):
        token: Optional[str] = request.headers.get("Authorization")

        if not token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in token:
            raise TokenTypeNotBearerError()

        token = token.replace("Bearer ", "")

        payload: PayloadDepartamentUserJWT = UtilsJWT.decode(
            token, App.http.configs.secret_key, class_=PayloadDepartamentUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        departament_finding_service: IService[
            DepartamentFindingUUIDServiceProps, Departament
        ] = DepartamentFindingUUIDService()

        agent_finding_service: IService[
            AgentFindingServiceProps, Agent
        ] = AgentFindingService()

        departament_finding_service_props: DepartamentFindingUUIDServiceProps = (
            DepartamentFindingUUIDServiceProps(
                departament_uuid=payload.uuid_departament
            )
        )

        departament: Departament = departament_finding_service.execute(
            departament_finding_service_props
        )

        agent_finding_service_props: AgentFindingServiceProps = (
            AgentFindingServiceProps(
                agent_uuid=payload.user_uuid, departament=departament
            )
        )

        agent: Agent = agent_finding_service.execute(agent_finding_service_props)

        return {"auth_user": agent, "auth_departament": departament}

    def catch(self, exception: Exception):
        validation: bool = isinstance(
            exception,
            (
                DepartamentNotFoundError,
                DepartamentNotFoundError,
                UserNotFoundError,
                ExpiredTokenError,
                AuthorizationNotFoundHeader,
            ),
        )

        if validation:
            return ResponseInauthorized(data=str(exception))

        raise exception
