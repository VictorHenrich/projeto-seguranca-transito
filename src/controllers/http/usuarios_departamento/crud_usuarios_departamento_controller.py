from typing import Dict, Any, List
from uuid import UUID
from dataclasses import dataclass

from start import app
from patterns.service import IService
from models import Agent, Departament
from server.http import Controller, ResponseDefaultJSON, ResponseSuccess
from middlewares.http import (
    BodyRequestValidationMiddleware,
    DepartamentUserAuthenticationMiddleware,
)
from services.agent import (
    AgentCriationService,
    AgentExclusionService,
    AgentListingService,
    AgentUpgradeService,
)


@dataclass
class DepartamentUserRegistrationRequestBody:
    nome: str
    usuario: str
    senha: str
    cargo: str


@app.http.add_controller(
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
        service: IService[List[Agent]] = AgentListingService()

        users: List[Agent] = service.execute(departament=auth_departament)

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
        service: IService[None] = AgentCriationService()

        service.execute(
            departament=auth_departament,
            name=body_request.nome,
            user=body_request.usuario,
            password=body_request.senha,
            position=body_request.cargo,
        )

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
        service: IService[None] = AgentUpgradeService()

        service.execute(
            departament=auth_departament,
            name=body_request.nome,
            user=body_request.usuario,
            password=body_request.senha,
            position=body_request.cargo,
            uuid_departament_user=str(user_hash),
        )

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    def delete(
        self,
        user_hash: UUID,
        auth_user: Agent,
        auth_departament: Departament,
    ) -> ResponseDefaultJSON:
        service: IService[None] = AgentExclusionService()

        service.execute(
            departament=auth_departament, uuid_departament_user=str(user_hash)
        )

        return ResponseSuccess()
