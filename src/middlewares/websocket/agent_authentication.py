from typing import Tuple, Dict, Union

from server.websocket import SocketMiddleware
from models import Agent, Departament
from patterns.service import IService
from services.agent import VerifyAgentAuthService, VerifyAgentAuthServiceProps
from server import App


class AgentAuthenticationMiddleware(SocketMiddleware[None]):
    def handle(self, props: None) -> Dict[str, Union[Agent, Departament]]:
        token: str = App.websocket.global_request.headers.get("Authorization") or ""

        verify_agent_auth_props: VerifyAgentAuthServiceProps = (
            VerifyAgentAuthServiceProps(token)
        )

        verify_agent_auth_service: IService[
            VerifyAgentAuthServiceProps, Tuple[Agent, Departament]
        ] = VerifyAgentAuthService()

        agent, departament = verify_agent_auth_service.execute(verify_agent_auth_props)

        return {"auth_user": agent, "auth_departament": departament}
