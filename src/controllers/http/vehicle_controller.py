from typing import Collection, Mapping, Any, TypeAlias
from flask import Response

from server.http import HttpServer, HttpController, ResponseSuccess
from middlewares.http import UserAuthenticationMiddleware
from models import User
from patterns.service import IService
from services.vehicle import VehicleListingService


DictCollectionType: TypeAlias = Collection[Mapping[str, Any]]


user_auth_middleware: UserAuthenticationMiddleware = UserAuthenticationMiddleware()


@HttpServer.add_controller("/user/vehicle/query")
class VehicleQueryController(HttpController):
    @user_auth_middleware.apply()
    def get(self, auth: User) -> Response:
        vehicle_listing_service: IService[DictCollectionType] = VehicleListingService(
            auth
        )

        vehicles: DictCollectionType = vehicle_listing_service.execute()

        return ResponseSuccess(data=vehicles)
