from dataclasses import dataclass

from server import HttpServer
from middlewares.http import BodyRequestValidationMiddleware, BodyRequestValidationProps
from patterns.service import IService
from exceptions import UserNotFoundError
from services.user import UserAuthenticationService
from server.http import (
    HttpController,
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseInauthorized,
)


@dataclass
class AuthUserRequestBody:
    email: str
    password: str


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)
body_request_props: BodyRequestValidationProps = BodyRequestValidationProps(
    AuthUserRequestBody
)


@HttpServer.add_controller(
    "/user/authentication",
)
class UserAuthController(HttpController):
    @body_request_middleware.apply(body_request_props)
    def post(self, body_request: AuthUserRequestBody) -> ResponseDefaultJSON:
        try:
            service: IService[str] = UserAuthenticationService(
                email=body_request.email, password=body_request.password
            )

            token: str = service.execute()

            return ResponseSuccess(data=token)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))
