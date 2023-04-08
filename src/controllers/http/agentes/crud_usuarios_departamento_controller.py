from typing import Dict, Any, List
from uuid import UUID
from dataclasses import dataclass

from server import App
from patterns.service import IService
from models import Agent, Departament
from server.http import Controller, ResponseDefaultJSON, ResponseSuccess
from middlewares.http import (
    BodyRequestValidationMiddleware,
    BodyRequestValidationProps,
    AgentAuthenticationMiddleware,
)
from services.agent import (
    AgentCreationService,
    AgentCreationServiceProps,
    AgentExclusionService,
    AgentExclusionServiceProps,
    AgentsFetchingService,
    AgentsFetchingServiceProps,
    AgentUpdateService,
    AgentUpdateServiceProps,
)


@dataclass
class DepartamentUserRegistrationRequestBody:
    nome: str
    usuario: str
    senha: str
    cargo: str


agent_auth_middleware: AgentAuthenticationMiddleware = AgentAuthenticationMiddleware()
body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)
body_request_props: BodyRequestValidationProps = BodyRequestValidationProps(
    DepartamentUserRegistrationRequestBody
)


@App.http.add_controller(
    "/departamento/usuario/crud",
    "/departamento/usuario/crud/<uuid:user_hash>",
)
class CrudUsuariosDepartamentosController(Controller):
    @agent_auth_middleware.apply(None)
    def get(
        self,
        auth_user: Agent,
        auth_departament: Departament,
    ) -> ResponseDefaultJSON:
        service: IService[
            AgentsFetchingServiceProps, List[Agent]
        ] = AgentsFetchingService()

        service_props: AgentsFetchingServiceProps = AgentsFetchingServiceProps(
            departament=auth_departament
        )

        users: List[Agent] = service.execute(service_props)

        response: List[Dict[str, Any]] = [
            {
                "uuid": user.id_uuid,
                "nome": user.nome,
                "cargo": user.cargo,
                "data_cadastro": str(user.data_cadastro),
            }
            for user in users
        ]

        return ResponseSuccess(data=response)

    @body_request_middleware.apply(body_request_props)
    def post(
        self,
        auth_user: Agent,
        auth_departament: Departament,
        body_request: DepartamentUserRegistrationRequestBody,
    ) -> ResponseDefaultJSON:
        service: IService[AgentCreationServiceProps, None] = AgentCreationService()

        service_props: AgentCreationServiceProps = AgentCreationServiceProps(
            departament=auth_departament,
            name=body_request.nome,
            access=body_request.usuario,
            password=body_request.senha,
            position=body_request.cargo,
        )

        service.execute(service_props)

        return ResponseSuccess()

    @agent_auth_middleware.apply(None)
    @body_request_middleware.apply(body_request_props)
    def put(
        self,
        user_hash: UUID,
        auth_user: Agent,
        auth_departament: Departament,
        body_request: DepartamentUserRegistrationRequestBody,
    ) -> ResponseDefaultJSON:
        service: IService[AgentUpdateServiceProps, None] = AgentUpdateService()

        service_props: AgentUpdateServiceProps = AgentUpdateServiceProps(
            departament=auth_departament,
            name=body_request.nome,
            access=body_request.usuario,
            password=body_request.senha,
            position=body_request.cargo,
            agent_uuid=auth_user.id_uuid,
        )

        service.execute(service_props)

        return ResponseSuccess()

    @agent_auth_middleware.apply(None)
    def delete(
        self,
        user_hash: UUID,
        auth_user: Agent,
        auth_departament: Departament,
    ) -> ResponseDefaultJSON:
        service: IService[AgentExclusionServiceProps, None] = AgentExclusionService()

        service_props: AgentExclusionServiceProps = AgentExclusionServiceProps(
            departament=auth_departament, agent_uuid=str(user_hash)
        )

        service.execute(service_props)

        return ResponseSuccess()
