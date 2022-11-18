from typing import Mapping, Any, Optional
from dataclasses import dataclass
from abc import ABC
from server.http import Controller, ResponseSuccess, ResponseDefaultJSON, ResponseFailure
from middlewares import DepartamentUserAuthenticationMiddleware, BodyRequestValidationMiddleware
from models import UsuarioDepartamento, Departamento, Nivel
from services.level import LevelRegistrationService
from services.level.entities import LevelRegistration
from exceptions import LevelNotFoundError



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

        niveis: list[Nivel] = LevelRepository.fetch(auth_departament)

        resposta_json: Mapping[str, Any] = [
            CRUDLevelView(
                descricao=n.descricao,
                nivel=n.nivel,
                uuid=n.id_uuid,
                obs=n.obs
            ).__dict__

            for n in niveis
        ]

        return ResponseSuccess(data=resposta_json)

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

        LevelRegistrationService.execute(param)

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
        try:
            LevelRepository.update(
                hash_level,
                auth_departament,
                body_request
            )

        except LevelNotFoundError as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    def delete(
        self,
        hash_level: str,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        try:
            LevelRepository.delete(hash_level, auth_departament)

        except LevelNotFoundError as error:
            return ResponseFailure(data=str(error))

        else:
            return ResponseSuccess()

            

            
