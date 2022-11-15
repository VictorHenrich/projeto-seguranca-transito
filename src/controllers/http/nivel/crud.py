from typing import Mapping, Any
from services.http import Controller, ResponseSuccess, ResponseDefaultJSON, ResponseFailure
from middlewares import DepartamentUserAuthenticationMiddleware, BodyRequestValidationMiddleware
from models import UsuarioDepartamento, Departamento, Nivel
from patterns.nivel.crud import LevelRegistration, LevelView
from repositories import LevelRepository
from exceptions import LevelNotFoundError




class CrudNivelController(Controller):
    @DepartamentUserAuthenticationMiddleware.apply()
    def get(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:

        niveis: list[Nivel] = LevelRepository.fetch(auth_departament)

        resposta_json: Mapping[str, Any] = [
            LevelView(
                descricao=n.descricao,
                nivel=n.nivel,
                uuid=n.id_uuid,
                obs=n.obs
            ).__dict__

            for n in niveis
        ]

        return ResponseSuccess(data=resposta_json)

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(LevelRegistration)
    def post(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: LevelRegistration
    ) -> ResponseDefaultJSON:
        LevelRepository.create(
            auth_departament,
            body_request
        )

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

            

            
