from typing import Optional
from datetime import datetime, timedelta

from start import server
from services.utils import UtilsJWT, Constants
from services.database import Database
from models import Usuario
from middlewares import BodyRequestValidationMiddleware
from patterns.autenticacao import PayloadJWT,  UserAuthentication
from exceptions import UserNotFoundError
from services.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseInauthorized,
    ResponseSuccess
)


db: Database = server.databases.get_database()


class AutenticacaoUsuarioController(Controller):
    @BodyRequestValidationMiddleware.apply()
    def post(
        self,
        body_request: UserAuthentication
    ) -> ResponseDefaultJSON:
        with db.create_session() as session:
            try:
                usuario: Optional[Usuario] = \
                    session\
                        .query(Usuario)\
                        .filter(
                            Usuario.email == body_request.email,
                            Usuario.senha == body_request.senha
                        )\
                        .first()

                if not usuario:
                    raise UserNotFoundError()

            except UserNotFoundError as error:
                return ResponseInauthorized(data=str(error))

            tempo_maximo: float = Constants.Authentication.max_minute_authenticated
            
            tempo_expiracao: float = (datetime.now() - timedelta(minutes=tempo_maximo)).timestamp()

            dados_autenticacao: PayloadJWT = PayloadJWT(usuario.id_uuid, tempo_expiracao)

            token: str = UtilsJWT.encode(dados_autenticacao.__dict__, server.http.configs.secret_key)

            return ResponseSuccess(data=f"Bearer {token}")

            



