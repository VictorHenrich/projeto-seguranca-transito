from datetime import datetime, timedelta

from start import app
from server.utils import UtilsJWT, Constants
from models import Usuario
from middlewares import BodyRequestValidationMiddleware
from patterns import InterfaceService
from exceptions import UserNotFoundError
from utils.entities import PayloadUserJWT
from services.user import UserAuthenticationService
from services.user.entities import UserAuthentication
from server.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseInauthorized
)


class AutenticacaoUsuarioController(Controller):
    @BodyRequestValidationMiddleware.apply(UserAuthentication)
    def post(
        self,
        body_request: UserAuthentication
    ) -> ResponseDefaultJSON:
        try:
            service: InterfaceService[UserAuthentication] = UserAuthenticationService()

            user: Usuario = service.execute(body_request)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))
            
        max_time: float = Constants.Authentication.max_minute_authenticated
        
        expired: float = (datetime.now() + timedelta(minutes=max_time)).timestamp()

        payload: PayloadUserJWT = PayloadUserJWT(user.id_uuid, expired)

        token: str = UtilsJWT.encode(payload.__dict__, app.http.configs.secret_key)

        return ResponseSuccess(data=f"Bearer {token}")

            



