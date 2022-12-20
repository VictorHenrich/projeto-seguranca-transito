from datetime import datetime, timedelta
from dataclasses import dataclass

from start import app
from server.utils import UtilsJWT, Constants
from models import Usuario
from middlewares import BodyRequestValidationMiddleware
from patterns.service import IService
from exceptions import UserNotFoundError
from utils.entities import PayloadUserJWT
from services.user import UserAuthenticationService
from server.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseInauthorized
)




@dataclass
class AuthUserRequestBody:
    email: str
    senha: str


class AutenticacaoUsuarioController(Controller):
    @BodyRequestValidationMiddleware.apply(AuthUserRequestBody)
    def post(
        self,
        body_request: AuthUserRequestBody
    ) -> ResponseDefaultJSON:
        try:
            service: IService[Usuario] = UserAuthenticationService()

            user: Usuario = service.execute(
                email=body_request.email,
                password=body_request.senha
            )

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))
            
        max_time: float = Constants.Authentication.max_minute_authenticated
        
        expired: float = (datetime.now() + timedelta(minutes=max_time)).timestamp()

        payload: PayloadUserJWT = PayloadUserJWT(user.id_uuid, expired)

        token: str = UtilsJWT.encode(payload.__dict__, app.http.configs.secret_key)

        return ResponseSuccess(data=f"Bearer {token}")

            



