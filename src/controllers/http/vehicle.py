from typing import Collection, Mapping, Any, TypeAlias
from uuid import UUID
from flask import Response

from server.http import HttpServer, HttpController, ResponseSuccess
from middlewares.http import (
    UserAuthenticationMiddleware,
    BodyRequestValidationMiddleware,
    BodyRequestValidationProps,
)
from models import User
from patterns.service import IService
from services.vehicle import (
    VehicleListingService,
    VehicleUpdateService,
    VehicleCreationService,
)
from utils.entities import VehiclePayload


DictCollectionType: TypeAlias = Collection[Mapping[str, Any]]


user_auth_middleware: UserAuthenticationMiddleware = UserAuthenticationMiddleware()

body_request_validation_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)


@HttpServer.add_controller("/user/vehicle/query")
class VehicleQueryController(HttpController):
    @user_auth_middleware.apply()
    def get(self, auth: User) -> Response:
        vehicle_listing_service: IService[DictCollectionType] = VehicleListingService(
            auth
        )

        vehicles: DictCollectionType = vehicle_listing_service.execute()

        return ResponseSuccess(data=vehicles)


@HttpServer.add_controller(
    "/user/vehicle/register", "/user/vehicle/register/<uuid:vehicle_hash>"
)
class VehicleRegisterController(HttpController):
    @user_auth_middleware.apply()
    @body_request_validation_middleware.apply(
        BodyRequestValidationProps(VehiclePayload)
    )
    def post(self, auth: User, body_request: VehiclePayload) -> Response:
        vehicle_creation_service: IService[None] = VehicleCreationService(
            auth, body_request
        )

        vehicle_creation_service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    @body_request_validation_middleware.apply(
        BodyRequestValidationProps(VehiclePayload)
    )
    def put(
        self, auth: User, body_request: VehiclePayload, vehicle_hash: UUID
    ) -> Response:
        vehicle_update_service: IService[None] = VehicleUpdateService(
            str(vehicle_hash), auth, body_request
        )

        vehicle_update_service.execute()

        return ResponseSuccess()
