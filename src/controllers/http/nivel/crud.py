from typing import Mapping, Any, Optional
from dataclasses import dataclass
from abc import ABC
from server.http import Controller, ResponseSuccess, ResponseDefaultJSON, ResponseFailure
from middlewares import DepartamentUserAuthenticationMiddleware, BodyRequestValidationMiddleware
from models import UsuarioDepartamento, Departamento, Nivel
from patterns import InterfaceService
from services.level import (
    LevelRegistrationService, 
    LevelUpgradeService,
    LevelExclusionService,
    LevelListingService
)
from services.level.entities import (
    LevelRegistration, 
    LevelLocation, 
    LevelUpdate
)





@dataclass
class CRUDLevelData(ABC):
    description: str
    level: int
    obs: Optional[str]



@dataclass
class CRUDLevelRegistration(CRUDLevelData):
    pass



@dataclass
class CRUDLevelView(CRUDLevelData):
    uuid: str



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
            CRUDLevelView(
                descricao=n.descricao,
                nivel=n.nivel,
                uuid=n.id_uuid,
                obs=n.obs
            ).__dict__

            for n in levels
        ]

        return ResponseSuccess(data=response)

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(CRUDLevelRegistration)
    def post(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: CRUDLevelRegistration
    ) -> ResponseDefaultJSON:
        
        param: LevelRegistration = LevelRegistration(
            body_request.description,
            body_request.level,
            body_request.obs,
            auth_departament
        )

        service: InterfaceService[LevelRegistration] = LevelRegistrationService()

        service.execute(param)

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(CRUDLevelRegistration)
    def put(
        self,
        hash_level: str,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: CRUDLevelRegistration
    ) -> ResponseDefaultJSON:

        data: LevelRegistration = LevelRegistration(
            body_request.description,
            body_request.level,
            body_request.obs
        )

        location_data: LevelLocation = LevelLocation(hash_level, auth_departament)

        param: LevelUpdate = LevelUpdate(data, location_data)

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

            

            
