from dataclasses import dataclass

from start import app
from middlewares import BodyRequestValidationMiddleware
from exceptions import DepartamentNotFoundError, UserNotFoundError
from services.departament_user import DepartamentUserAuthorizationService
from patterns.service import IService
from server.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseInauthorized,
    ResponseSuccess,
)


@dataclass
class DepartamentUserAuthRequestBody:
    departamento: str
    usuario: str
    senha: str


@app.http.add_controller("/autenticacao/departamento")
class AutenticaoUsuarioDepartamentoController(Controller):
    @BodyRequestValidationMiddleware.apply(DepartamentUserAuthRequestBody)
    def post(self, body_request: DepartamentUserAuthRequestBody) -> ResponseDefaultJSON:

        try:
            service: IService[str] = DepartamentUserAuthorizationService()

            token: str = service.execute(
                departament_access=body_request.departamento,
                user=body_request.usuario,
                password=body_request.senha,
            )

            return ResponseSuccess(data=token)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))

        except DepartamentNotFoundError as error:
            return ResponseInauthorized(data=str(error))
