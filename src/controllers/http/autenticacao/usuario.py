from dataclasses import dataclass

from server import App
from middlewares.http import BodyRequestValidationMiddleware
from patterns.service import IService
from exceptions import UserNotFoundError
from services.user import UserAuthenticationService, UserAuthenticationServiceProps
from server.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseInauthorized,
)


@dataclass
class AuthUserRequestBody:
    email: str
    senha: str


@App.http().add_controller(
    "/autenticacao/usuario",
)
class AutenticacaoUsuarioController(Controller):
    @BodyRequestValidationMiddleware.apply(AuthUserRequestBody)
    def post(self, body_request: AuthUserRequestBody) -> ResponseDefaultJSON:
        try:
            service: IService[
                UserAuthenticationServiceProps, str
            ] = UserAuthenticationService()

            service_props: UserAuthenticationServiceProps = (
                UserAuthenticationServiceProps(
                    email=body_request.email, password=body_request.senha
                )
            )

            token: str = service.execute(service_props)

            return ResponseSuccess(data=token)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))
