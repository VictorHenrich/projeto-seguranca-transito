from dataclasses import dataclass

from start import app
from middlewares.http import BodyRequestValidationMiddleware
from patterns.service import IService
from exceptions import UserNotFoundError
from services.user import UserAuthenticationService
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


@app.http.add_controller("/autenticacao/usuario")
class AutenticacaoUsuarioController(Controller):
    @BodyRequestValidationMiddleware.apply(AuthUserRequestBody)
    def post(self, body_request: AuthUserRequestBody) -> ResponseDefaultJSON:
        try:
            service: IService[str] = UserAuthenticationService()

            token: str = service.execute(
                email=body_request.email, password=body_request.senha
            )

            return ResponseSuccess(data=token)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))
