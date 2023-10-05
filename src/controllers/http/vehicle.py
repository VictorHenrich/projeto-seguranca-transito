from typing import Collection, Mapping, Any, TypeAlias, Optional
from uuid import UUID
from flask import Response
from dataclasses import dataclass

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
    VehicleExclusionService,
)
from utils.entities import VehiclePayload
from utils.types import VehicleTypes, DictType


DictCollectionType: TypeAlias = Collection[DictType]


user_auth_middleware: UserAuthenticationMiddleware = UserAuthenticationMiddleware()

body_request_validation_middleware: BodyRequestValidationMiddleware = (
    BodyRequestValidationMiddleware()
)


@dataclass
class VehicleBody:
    plate: str
    renavam: str
    vehicle_type: str
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    chassi: Optional[str] = None
    have_safe: bool = False


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
    @body_request_validation_middleware.apply(BodyRequestValidationProps(VehicleBody))
    def post(self, auth: User, body_request: VehicleBody) -> Response:
        vehicle_payload: VehiclePayload = VehiclePayload(
            body_request.plate,
            body_request.renavam,
            VehicleTypes(body_request.vehicle_type),
            body_request.brand,
            body_request.model,
            body_request.color,
            body_request.year,
            body_request.chassi,
            body_request.have_safe,
        )

        vehicle_creation_service: IService[DictType] = VehicleCreationService(
            auth, vehicle_payload
        )

        vehicle_creation_service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    @body_request_validation_middleware.apply(BodyRequestValidationProps(VehicleBody))
    def put(
        self, auth: User, body_request: VehicleBody, vehicle_hash: UUID
    ) -> Response:
        vehicle_payload: VehiclePayload = VehiclePayload(
            body_request.plate,
            body_request.renavam,
            VehicleTypes(body_request.vehicle_type),
            body_request.brand,
            body_request.model,
            body_request.color,
            body_request.year,
            body_request.chassi,
            body_request.have_safe,
        )

        vehicle_update_service: IService[DictType] = VehicleUpdateService(
            str(vehicle_hash), auth, vehicle_payload
        )

        vehicle_update_service.execute()

        return ResponseSuccess()

    @user_auth_middleware.apply()
    def delete(self, auth: User, vehicle_hash: UUID) -> Response:
        vehicle_exclusion_service: IService[None] = VehicleExclusionService(
            str(vehicle_hash), auth
        )

        vehicle_exclusion_service.execute()

        return ResponseSuccess()
