from typing import Tuple

from server import App
from server.http import HttpMiddleware, ResponseInauthorized
from models import Agent, Departament
from patterns.service import IService
from services.agent import VerifyAgentAuthService, VerifyAgentAuthServiceProps
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
    DepartamentNotFoundError,
)
from server import App


class AgentAuthenticationMiddleware(HttpMiddleware[None]):
    def handle(self, props: None):
        token: str = App.http.global_request.headers.get("Authorization") or ""

        verify_agent_auth_props: VerifyAgentAuthServiceProps = (
            VerifyAgentAuthServiceProps(token)
        )

        verify_agent_auth_service: IService[
            VerifyAgentAuthServiceProps, Tuple[Agent, Departament]
        ] = VerifyAgentAuthService()

        agent, departament = verify_agent_auth_service.execute(verify_agent_auth_props)

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
                TokenTypeNotBearerError,
            ),
        )

        if validation:
            return ResponseInauthorized(data=str(exception))

        raise exception
