from dataclasses import dataclass

from server import HttpServer
from middlewares.http import BodyRequestValidationMiddleware, BodyRequestValidationProps
from patterns.service import IService
from exceptions import UserNotFoundError, ExpiredTokenError
from services.authentication import AuthenticationService, AuthRefreshService
from server.http import (
    HttpController,
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseInauthorized,
)
from utils.entities import UserAuthPayload


@dataclass
class AuthRefreshBody:
    token: str


body_request_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)

auth_body_request: BodyRequestValidationProps = BodyRequestValidationProps(
    UserAuthPayload
)

auth_refresh_body_request: BodyRequestValidationProps = BodyRequestValidationProps(
    AuthRefreshBody
)


@HttpServer.add_controller(
    "/user/authentication",
)
class AuthenticationController(HttpController):
    @body_request_middleware.apply(auth_body_request)
    def post(self, body_request: UserAuthPayload) -> ResponseDefaultJSON:
        try:
            service: IService[str] = AuthenticationService(credentials=body_request)

            token: str = service.execute()

            return ResponseSuccess(data=token)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))


@HttpServer.add_controller("/user/authentication/refresh")
class AuthenticationRefreshController(HttpController):
    @body_request_middleware.apply(auth_refresh_body_request)
    def post(self, body_request: AuthRefreshBody) -> ResponseDefaultJSON:
        try:
            service: IService[str] = AuthRefreshService(body_request.token)

            token: str = service.execute()

            return ResponseSuccess(data=token)

        except ExpiredTokenError as error:
            return ResponseInauthorized(data=str(error))
