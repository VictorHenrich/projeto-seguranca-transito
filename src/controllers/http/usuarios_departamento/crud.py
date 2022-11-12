from typing import Optional, Mapping, Any
from uuid import UUID

from start import server
from services.database import Database
from models import UsuarioDepartamento, Departamento
from patterns.usuario_departamento import DepartamentUserRegistration, DepartamentUserView
from exceptions import UserNotFoundError
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
        with db.create_session() as session:
            usuarios: list[UsuarioDepartamento] = \
                session\
                    .query(UsuarioDepartamento)\
                    .join(UsuarioDepartamento.id_departamento == Departamento.id)\
                    .filter(Departamento.id == auth_departament.id)\
                    .all()

            lista_usuarios_json: list[Mapping[str, Any]] = [
                DepartamentUserView(usuario.nome).__dict__
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
        with db.create_session() as session:
            usuario: UsuarioDepartamento = UsuarioDepartamento()

            usuario.acesso = body_request.usuario
            usuario.cargo = body_request.cargo
            usuario.senha = body_request.senha
            usuario.id_departamento = auth_departament.id
            
            session.add(usuario)
            session.commit()

            return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistration)
    def put(
        self,
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: DepartamentUserRegistration,
        user_hash: UUID 
    ) -> ResponseDefaultJSON:
        with db.create_session() as session:
            try:
                usuario: Optional[UsuarioDepartamento] = \
                    session\
                        .query(UsuarioDepartamento)\
                        .filter(UsuarioDepartamento.id_uuid == str(user_hash))\
                        .first()

                if not usuario:
                    raise UserNotFoundError()

            except UserNotFoundError as error:
                return ResponseFailure(data=str(error))

            usuario.acesso = body_request.usuario
            usuario.nome = body_request.nome
            usuario.cargo = body_request.cargo
            usuario.senha = body_request.senha
            
            session.add(usuario)
            session.commit()

            return ResponseSuccess()

    @DepartamentUserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(DepartamentUserRegistration)
    def delete(
        auth_user: UsuarioDepartamento,
        auth_departament: Departamento,
        body_request: DepartamentUserRegistration,
        user_hash: UUID 
    ) -> ResponseDefaultJSON:
        with db.create_session() as session:
            try:
                usuario: Optional[UsuarioDepartamento] = \
                    session\
                        .query(UsuarioDepartamento)\
                        .filter(UsuarioDepartamento.id_uuid == str(user_hash))\
                        .first()

                if not usuario:
                    raise UserNotFoundError()

            except UserNotFoundError as error:
                return ResponseFailure(data=str(error))

            session.delete(usuario)
            session.commit()

            return ResponseSuccess()