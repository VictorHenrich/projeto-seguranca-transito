from typing import Mapping, Any
from uuid import UUID

from models import UsuarioDepartamento, Departamento
from repositories import DepartamentUserRepository
from server.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseSuccess
)
from middlewares import (
    BodyRequestValidationMiddleware, 
    DepartamentUserAuthenticationMiddleware
)
from patterns import InterfaceService
from services.departament_user import (
    DepartamentUserCriationService,
    DepartamentUserExclusionService,
    DepartamentUserListingService,
    DepartamentUserUpgradeService
)
from services.departament_user.entities import (
    DepartamentUserLocation,
    DepartamentUserRegistration,
    DepartamentUserUpgrade
)



class CrudUsuariosDepartamentosController(Controller):
    @DepartamentUserAuthenticationMiddleware.apply()
    def get(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        location: DepartamentUserLocation = DepartamentUserLocation(
            auth_user.id_uuid,
            auth_departament
        )

        service: InterfaceService[DepartamentUserLocation] = DepartamentUserListingService()

        users: list[UsuarioDepartamento] = service.execute(location)

        response: list[Mapping[str, Any]] = [
            {
                "uuid": user.id_uuid,
                "nome": user.nome,
                "cargo": user.cargo,
                "data_cadastro": user.data_cadastro,
            }

            for user in users
        ]

        return ResponseSuccess(data=response)

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistration)
    def post(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: DepartamentUserRegistration
    ) -> ResponseDefaultJSON:
        service: InterfaceService[DepartamentUserRegistration] = DepartamentUserCriationService()

        body_request.departament = auth_departament

        service.execute(body_request)

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistration)
    def put(
        self,
        user_hash: UUID,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: DepartamentUserRegistration,
    ) -> ResponseDefaultJSON:
        location: DepartamentUserLocation = DepartamentUserLocation(
            user_hash,
            auth_departament
        )

        param: DepartamentUserUpgrade = DepartamentUserUpgrade(
            body_request,
            location
        )

        service: InterfaceService[DepartamentUserUpgrade] = DepartamentUserUpgradeService()

        service.execute(param)

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    def delete(
        self,
        user_hash: UUID,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        location: DepartamentUserLocation = DepartamentUserLocation(
            user_hash,
            auth_departament
        )

        service: InterfaceService[DepartamentUserLocation] = DepartamentUserExclusionService()

        service.execute(location)

        return ResponseSuccess()

