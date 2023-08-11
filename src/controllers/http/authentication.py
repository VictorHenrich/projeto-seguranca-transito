from dataclasses import dataclass

from server import HttpServer
from middlewares.http import BodyRequestValidationMiddleware, BodyRequestValidationProps
from patterns.service import IService
from exceptions import UserNotFoundError
from services.authentication import AuthenticationService, AuthRefreshService
from server.http import (
    HttpController,
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseInauthorized,
)


@dataclass
class AuthBody:
    email: str
    password: str


@dataclass
class AuthRefreshBody:
    token: str


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)

auth_body_request: BodyRequestValidationProps = BodyRequestValidationProps(AuthBody)

auth_refresh_body_request: BodyRequestValidationProps = BodyRequestValidationProps(
    AuthRefreshBody
)


@HttpServer.add_controller(
    "/user/authentication",
)
class AuthenticationController(HttpController):
    @body_request_middleware.apply(auth_body_request)
    def post(self, body_request: AuthBody) -> ResponseDefaultJSON:
        try:
            service: IService[str] = AuthenticationService(
                email=body_request.email, password=body_request.password
            )

            token: str = service.execute()

            return ResponseSuccess(data=token)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))


@HttpServer.add_controller("/user/authentication/refresh")
class AuthenticationRefreshController(HttpController):
    @body_request_middleware.apply(auth_body_request)
    def post(self, body_request: AuthRefreshBody) -> ResponseDefaultJSON:
        try:
            service: IService[str] = AuthRefreshService(body_request.token)

            token: str = service.execute()

            return ResponseSuccess(data=token)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))
