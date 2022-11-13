from typing import Mapping, Any
from uuid import UUID

from start import server
from services.database import Database
from models import UsuarioDepartamento, Departamento
from patterns.usuario_departamento import DepartamentUserRegistration, DepartamentUserView
from exceptions import UserNotFoundError
from repositories import DepartamentUserRepository
from services.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseFailure,
    ResponseSuccess
)
from middlewares import (
    BodyRequestValidationMiddleware, 
    DepartamentUserAuthenticationMiddleware
)



db: Database = server.databases.get_database()


class CrudUsuariosDepartamentosController(Controller):
    @DepartamentUserAuthenticationMiddleware.apply()
    def get(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        usuarios: list[UsuarioDepartamento] = \
            DepartamentUserRepository.list(id_departamento=auth_departament.id)

        lista_usuarios_json: list[Mapping[str, Any]] = [
            DepartamentUserView(
                usuario.nome, 
                usuario.cargo,
                usuario.id_uuid,
            ).__dict__
            
            for usuario in usuarios
        ]

        return ResponseSuccess(data=lista_usuarios_json)

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistration)
    def post(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: DepartamentUserRegistration
    ) -> ResponseDefaultJSON:

        DepartamentUserRepository.create(
            body_request.nome,
            body_request.usuario,
            body_request.cargo,
            body_request.senha,
            auth_departament.id
        )

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
        try:
            DepartamentUserRepository.update(
                uuid=str(user_hash),
                nome=body_request.nome,
                usuario=body_request.usuario,
                cargo=body_request.cargo,
                senha=body_request.senha
            )

        except UserNotFoundError as error:
            return ResponseFailure(data=str(error))

        return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    def delete(
        self,
        user_hash: UUID,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
    ) -> ResponseDefaultJSON:
        try:
            DepartamentUserRepository.delete(uuid=str(user_hash))

        except UserNotFoundError as error:
            return ResponseSuccess(data=str(error))

        return ResponseSuccess()