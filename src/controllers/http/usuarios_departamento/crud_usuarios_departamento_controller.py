from typing import Mapping, Any, List
from uuid import UUID
from dataclasses import dataclass

from patterns.service import IService
from models import UsuarioDepartamento, Departamento
from server.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseSuccess
)
from middlewares import (
    BodyRequestValidationMiddleware, 
    DepartamentUserAuthenticationMiddleware
)
from services.departament_user import (
    DepartamentUserCriationService,
    DepartamentUserExclusionService,
    DepartamentUserListingService,
    DepartamentUserUpgradeService
)



@dataclass
class DepartamentUserRegistrationRequestBody:
    nome: str
    usuario: str
    senha: str
    cargo: str


class CrudUsuariosDepartamentosController(Controller):
    @DepartamentUserAuthenticationMiddleware.apply()
    def get(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        service: IService[List[UsuarioDepartamento]] = DepartamentUserListingService()

        users: List[UsuarioDepartamento] = service.execute(
            departament=auth_departament
        )

        response: List[Mapping[str, Any]] = [
            {
                "uuid": user.id_uuid,
                "nome": user.nome,
                "cargo": user.cargo,
                "data_cadastro": str(user.data_cadastro)
            }

            for user in users
        ]

        return ResponseSuccess(data=response)

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistrationRequestBody)
    def post(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: DepartamentUserRegistrationRequestBody
    ) -> ResponseDefaultJSON:
        service: IService[None] = DepartamentUserCriationService()

        service.execute(
            departament=auth_departament,
            name=body_request.nome,
            user=body_request.usuario,
            password=body_request.senha,
            position=body_request.cargo
        )

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistrationRequestBody)
    def put(
        self,
        user_hash: UUID,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: DepartamentUserRegistrationRequestBody,
    ) -> ResponseDefaultJSON:
        service: IService[None] = DepartamentUserUpgradeService()

        service.execute(
            departament=auth_departament,
            name=body_request.nome,
            user=body_request.usuario,
            password=body_request.senha,
            position=body_request.cargo,
            uuid_departament_user=str(user_hash)
        )

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    def delete(
        self,
        user_hash: UUID,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        service: IService[None] = DepartamentUserExclusionService()

        service.execute(
            departament=auth_departament,
            uuid_departament_user=str(user_hash)
        )

        return ResponseSuccess()

