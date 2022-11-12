from start import server
from services.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseFailure
)
from services.database import Database
from middlewares import UserBodyAuthentication, UserAuthentication
from models import Usuario
from exceptions import UserNotFoundError
from patterns.usuario.crud import UserRegistration



db: Database = server.databases.get_database()


class CrudUsusarios(Controller):

    @UserBodyAuthentication.apply(UserRegistration)
    def post(self, body_request: UserRegistration) -> ResponseDefaultJSON:
        with db.create_session() as session:
            usuario: Usuario = Usuario()

            usuario.nome = body_request.nome
            usuario.email = body_request.email
            usuario.cpf = body_request.cpf
            usuario.senha = body_request.senha
            usuario.data_nascimento = body_request.data_nascimento

            session.add(usuario)

        return ResponseSuccess()

    @UserAuthentication.apply()
    @UserBodyAuthentication.apply(UserRegistration)
    def put(self, auth: Usuario, body_request: UserRegistration) -> ResponseDefaultJSON:

        with db.create_session() as session:
            try:
                usuario: Usuario = \
                    session\
                        .query(Usuario)\
                        .filter(Usuario.id_uuid == auth.id_uuid)\
                        .first()

                if not usuario:
                    raise UserNotFoundError()

            except UserNotFoundError as error:
                return ResponseFailure(data=str(error))

            usuario.email = body_request.email
            usuario.cpf = body_request.cpf
            usuario.data_nascimento = body_request.data_nascimento
            usuario.senha = body_request.senha

            session.add(usuario)

        return ResponseSuccess()

    @UserAuthentication.apply()
    def delete(self, auth: Usuario) -> ResponseDefaultJSON:
        with db.create_session() as session:
            try:
                usuario: Usuario = \
                    session\
                        .query(Usuario)\
                        .filter(Usuario.id_uuid == str(auth.id_uuid))\
                        .first()

                if not usuario:
                    raise UserNotFoundError()

            except UserNotFoundError as error:
                return ResponseFailure(data=str(error))

            session.delete(usuario)

            return ResponseSuccess()
