from dataclasses import dataclass

from server import App
from middlewares.http import BodyRequestValidationMiddleware, BodyRequestValidationProps
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


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)
body_request_props: BodyRequestValidationProps = BodyRequestValidationProps(
    AuthUserRequestBody
)


@App.http.add_controller(
    "/autenticacao/usuario",
)
class UserAuthController(Controller):
    @body_request_middleware.apply(body_request_props)
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
