from typing import Optional
from datetime import datetime, timedelta

from start import server
from services.utils import UtilsJWT, Constants
from services.database import Database
from models import UsuarioDepartamento, Departamento
from middlewares import BodyRequestValidationMiddleware
from patterns.autenticacao import PayloadJWT,  DepartamentUserAuthentication
from exceptions import DepartamentNotFoundError, UserNotFoundError
from repositories import DepartamentRepository, DepartamentUserRepository
from services.http import (
    Controller, 
    ResponseDefaultJSON,
    ResponseInauthorized,
    ResponseSuccess
)


db: Database = server.databases.get_database()


class AutenticaoUsuarioDepartamentoController(Controller):

    @BodyRequestValidationMiddleware.apply(DepartamentUserAuthentication)
    def post(
        self,
        body_request: DepartamentUserAuthentication
    ) -> ResponseDefaultJSON:

        try:
            departamento: Departamento = DepartamentRepository.get(
                acesso=body_request.departamento
            )

        except DepartamentNotFoundError as error:
            return ResponseInauthorized(data=str(error))

        try:
            usuario: UsuarioDepartamento = DepartamentUserRepository.get(
                usuario=body_request.usuario,
                senha=body_request.senha,
                id_departamento=departamento.id
            )

        except UserNotFoundError:
            return ResponseInauthorized(data=str(error))


        tempo_expiracao: float = \
            (datetime.now() + timedelta(minutes=Constants.Authentication.max_minute_authenticated)).timestamp()

        dados_autenticacao: PayloadJWT = PayloadJWT(usuario.id_uuid, tempo_expiracao)

        token: str = UtilsJWT.encode(dados_autenticacao.__dict__, server.http.application.secret_key)

        return ResponseSuccess(data=f"Bearer {token}")