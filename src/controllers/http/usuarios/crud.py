from typing import Mapping, Any

from start import app
from server.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseSuccess,
)
from middlewares import BodyRequestValidationMiddleware, UserAuthenticationMiddleware
from models import Usuario
from patterns import InterfaceService
from services.user import (
    UserLoadingService,
    UserExclusionService,
    UserRegistrationService,
    UserUpgradeService
)
from services.user.entities import (
    UserLocation,
    UserRegistration,
    UserUpgrade
)



class CrudUsuariosController(Controller):

    @BodyRequestValidationMiddleware.apply(UserRegistration)
    def post(self, body_request: UserRegistration) -> ResponseDefaultJSON:
        service: InterfaceService[UserRegistration] = UserRegistrationService()

        service.execute(body_request)

    @UserAuthenticationMiddleware.apply()
    @BodyRequestValidationMiddleware.apply(UserRegistration)
    def put(self, auth: Usuario, body_request: UserRegistration) -> ResponseDefaultJSON:
        location_data: UserLocation = UserLocation(auth.id_uuid)

        data: UserUpgrade = UserUpgrade(body_request, location_data)

        service: InterfaceService[UserUpgrade] = UserUpgradeService()

        service.execute(data)

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def delete(self, auth: Usuario) -> ResponseDefaultJSON:
        location_data: UserLocation = UserLocation(auth.id_uuid)

        service: InterfaceService[UserLocation] = UserExclusionService()

        service.execute(location_data)

        return ResponseSuccess()

    @UserAuthenticationMiddleware.apply()
    def get(self,  auth: Usuario) -> ResponseDefaultJSON:
        location_data: UserLocation = UserLocation(auth.id_uuid)

        service: InterfaceService[UserLocation] = UserLoadingService()
        
        user: Usuario = service.execute(location_data)

        response: Mapping[str, Any] = {
            "nome": user.nome,
            "email": user.email,
            "cpf": user.cpf,
            "uuid": user.id_uuid,
            "data_nascimento": user.data_nascimento
        }

        return ResponseSuccess(data=response)
