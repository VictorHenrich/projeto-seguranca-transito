from typing import Dict, Any, List
from uuid import UUID
from dataclasses import dataclass

from server import App
from patterns.service import IService
from models import Agent, Departament
from server.http import Controller, ResponseDefaultJSON, ResponseSuccess
from middlewares.http import (
    BodyRequestValidationMiddleware,
    DepartamentUserAuthenticationMiddleware,
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


@App.http.add_controller(
    "/departamento/usuario/crud",
    "/departamento/usuario/crud/<uuid:user_hash>",
)
class CrudUsuariosDepartamentosController(Controller):
    @DepartamentUserAuthenticationMiddleware.apply()
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

    # @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistrationRequestBody)
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

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistrationRequestBody)
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
            departament_user=auth_user,
        )

        service.execute(service_props)

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
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
