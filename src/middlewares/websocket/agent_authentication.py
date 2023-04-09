from typing import Optional, Dict, Union
from datetime import datetime

from server.websocket import SocketMiddleware
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
)
from utils.entities import PayloadDepartamentUserJWT
from server import App


class AgentAuthenticationMiddleware(SocketMiddleware[None]):
    def handle(self, props: None) -> Dict[str, Union[Agent, Departament]]:
        token: Optional[str] = App.websocket.global_request.headers.get("Authorization")

        if not token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in token:
            raise TokenTypeNotBearerError()

        token = token.replace("Bearer ", "")

        payload: PayloadDepartamentUserJWT = UtilsJWT.decode(
            token, App.http.configs.secret_key, PayloadDepartamentUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        departament_service: IService[
            DepartamentFindingUUIDServiceProps, Departament
        ] = DepartamentFindingUUIDService()

        agent_service: IService[AgentFindingServiceProps, Agent] = AgentFindingService()

        departament_service_props: DepartamentFindingUUIDServiceProps = (
            DepartamentFindingUUIDServiceProps(
                departament_uuid=payload.uuid_departament
            )
        )

        departament: Departament = departament_service.execute(
            departament_service_props
        )

        agent_service_props: AgentFindingServiceProps = AgentFindingServiceProps(
            agent_uuid=payload.user_uuid, departament=departament
        )

        agent: Agent = agent_service.execute(agent_service_props)

        return {"auth_user": agent, "auth_departament": departament}
