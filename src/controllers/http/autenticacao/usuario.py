from typing import Optional
from datetime import datetime, timedelta

from start import app
from server.utils import UtilsJWT, Constants
from server.database import Database
from models import Usuario
from middlewares import BodyRequestValidationMiddleware
from patterns.autenticacao import PayloadJWT,  UserAuthentication
from exceptions import UserNotFoundError
from repositories import UserRepository
from server.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseSuccess,
    ResponseInauthorized
)



db: Database = app.databases.get_database()


class AutenticacaoUsuarioController(Controller):
    @BodyRequestValidationMiddleware.apply(UserAuthentication)
    def post(
        self,
        body_request: UserAuthentication
    ) -> ResponseDefaultJSON:
        try:
            usuario: Usuario = UserRepository.get(
                email=body_request.email,
                senha=body_request.senha
            )

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))
            
        tempo_maximo: float = Constants.Authentication.max_minute_authenticated
        
        tempo_expiracao: float = (datetime.now() + timedelta(minutes=tempo_maximo)).timestamp()

        dados_autenticacao: PayloadJWT = PayloadJWT(usuario.id_uuid, tempo_expiracao)

        token: str = UtilsJWT.encode(dados_autenticacao.__dict__, app.http.configs.secret_key)

        return ResponseSuccess(data=f"Bearer {token}")

            



