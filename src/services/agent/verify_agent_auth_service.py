from typing import Tuple
from dataclasses import dataclass
from datetime import datetime


from server import App
from server.utils import UtilsJWT
from models import Agent, Departament
from patterns.service import IService
from .agent_finding_service import AgentFindingService, AgentFindingServiceProps
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
)
from services.departament import (
    DepartamentFindingUUIDService,
    DepartamentFindingUUIDServiceProps,
)
from utils.entities import PayloadDepartamentUserJWT


@dataclass
class VerifyAgentAuthServiceProps:
    token: str


class VerifyAgentAuthService:
    def execute(self, props: VerifyAgentAuthServiceProps) -> Tuple[Agent, Departament]:
        if not props.token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in props.token:
            raise TokenTypeNotBearerError()

        token = props.token.replace("Bearer ", "")

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

        return agent, departament
