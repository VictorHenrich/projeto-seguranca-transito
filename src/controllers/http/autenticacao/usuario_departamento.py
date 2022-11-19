from datetime import datetime, timedelta

from start import app
from server.utils import UtilsJWT, Constants
from server.database import Database
from models import UsuarioDepartamento, Departamento
from middlewares import BodyRequestValidationMiddleware
from exceptions import DepartamentNotFoundError, UserNotFoundError
from services.departament_user import DepartamentUserAuthorizationService
from services.departament_user.entities import DepartamentUserAuthorization
from patterns import InterfaceService
from utils.entities import PayloadDepartamentUserJWT
from server.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseInauthorized,
    ResponseSuccess
)


db: Database = app.databases.get_database()


class AutenticaoUsuarioDepartamentoController(Controller):

    @BodyRequestValidationMiddleware.apply(DepartamentUserAuthorization)
    def post(
        self,
        body_request: DepartamentUserAuthorization
    ) -> ResponseDefaultJSON:

        try:
            service: InterfaceService[DepartamentUserAuthorization] = DepartamentUserAuthorizationService()

            departament, user = service.execute(body_request)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))

        except DepartamentNotFoundError as error:
            return ResponseInauthorized(data=str(error))


        expired: float = \
            (datetime.now() + timedelta(minutes=Constants.Authentication.max_minute_authenticated)).timestamp()

        payload: PayloadDepartamentUserJWT = PayloadDepartamentUserJWT(
            user.id_uuid,
            departament.id_uuid,
            expired
        )

        token: str = UtilsJWT.encode(
            payload.__dict__, 
            app.http.application.secret_key
        )

        return ResponseSuccess(data=f"Bearer {token}")