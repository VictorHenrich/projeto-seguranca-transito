from start import app
from server.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseFailure
)
from server.database import Database
from middlewares import BodyRequestValidationMiddleware, UserAuthenticationMiddleware
from models import Usuario
from exceptions import UserNotFoundError
from patterns.usuario.crud import UserRegistration
from repositories import UserRepository



db: Database = app.databases.get_database()


class CrudUsuariosController(Controller):

    @BodyRequestValidationMiddleware.apply(UserRegistration)
    def post(self, body_request: UserRegistration) -> ResponseDefaultJSON:
        UserRepository.create(
            nome=body_request.nome,
            email=body_request.email,
            cpf=body_request.cpf,
            senha=body_request.senha,
            data_nascimento=body_request.data_nascimento
        )

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(UserRegistration)
    def put(self, auth: Usuario, body_request: UserRegistration) -> ResponseDefaultJSON:
        try:
            UserRepository.update(
                id=auth.id,
                nome=body_request.nome,
                email=body_request.email,
                cpf=body_request.cpf,
                senha=body_request.senha,
                data_nascimento=body_request.data_nascimento
            )

        except UserNotFoundError as error:
            return ResponseFailure(data=str(error))

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def delete(self, auth: Usuario) -> ResponseDefaultJSON:
        try:
            UserRepository.delete(auth.id)

        except UserNotFoundError as error:
            return ResponseFailure(data=str(error))

        return ResponseSuccess()
