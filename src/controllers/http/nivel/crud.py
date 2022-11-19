from typing import Mapping, Any
from abc import ABC
from server.http import Controller, ResponseSuccess, ResponseDefaultJSON
from middlewares import DepartamentUserAuthenticationMiddleware, BodyRequestValidationMiddleware
from models import UsuarioDepartamento, Departamento, Nivel
from patterns import InterfaceService
from services.level import (
    LevelCriationService, 
    LevelUpgradeService,
    LevelExclusionService,
    LevelListingService
)
from services.level.entities import (
    LevelRegistration, 
    LevelLocation, 
    LevelUpdate
)



class CrudNivelController(Controller):
    @DepartamentUserAuthenticationMiddleware.apply()
    def get(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:

        param: LevelLocation = LevelLocation('', auth_departament)

        service: LevelListingService = LevelListingService()

        levels: list[Nivel] = service.execute(param)

        response: Mapping[str, Any] = [

            {
                "uuid": level.id_uuid,
                "descricao": level.descricao,
                "nivel": level.nivel,
                "obs": level.obs
            }

            for level in levels
        ]

        return ResponseSuccess(data=response)

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(LevelRegistration)
    def post(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: LevelRegistration
    ) -> ResponseDefaultJSON:
        service: InterfaceService[LevelRegistration] = LevelCriationService()

        body_request.departament = auth_departament

        service.execute(body_request)

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(LevelRegistration)
    def put(
        self,
        hash_level: str,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: LevelRegistration
    ) -> ResponseDefaultJSON:
        location_data: LevelLocation = LevelLocation(hash_level, auth_departament)

        param: LevelUpdate = LevelUpdate(body_request, location_data)

        service: InterfaceService[LevelUpdate] = LevelUpgradeService()

        service.execute(param)

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    def delete(
        self,
        hash_level: str,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        param: LevelLocation = LevelLocation(hash_level, auth_departament)

        service: LevelExclusionService = LevelExclusionService()

        service.execute(param)

        return ResponseSuccess()

            

            
