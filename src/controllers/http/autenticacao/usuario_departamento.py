from typing import Optional
from datetime import datetime, timedelta

from start import server
from services.utils import UtilsJWT, Constants
from services.database import Database
from models import UsuarioDepartamento, Departamento
from middlewares import BodyRequestValidationMiddleware
from patterns.autenticacao import PayloadJWT,  DepartamentUserAuthentication
from exceptions import DepartamentNotFoundError, UserNotFoundError
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

        with db.create_session() as session:
            try:
                departamento: Optional[Departamento] = \
                    session\
                        .query(Departamento)\
                        .filter(Departamento.acesso == body_request.departamento)\
                        .first()

                if not departamento:
                    raise DepartamentNotFoundError()

            except DepartamentNotFoundError as error:
                return ResponseInauthorized(data=str(error))

            try:
                usuario: Optional[UsuarioDepartamento] = \
                    session\
                        .query(UsuarioDepartamento)\
                        .filter(
                            UsuarioDepartamento.nome == body_request.usuario,
                            UsuarioDepartamento.senha == body_request.senha,
                            UsuarioDepartamento.id_departamento == departamento.id
                        )\
                        .first()

                if not usuario:
                    raise UserNotFoundError()

            except UserNotFoundError:
                return ResponseInauthorized(data=str(error))


            tempo_expiracao: float = \
                (datetime.now() - timedelta(minutes=Constants.Authentication.max_minute_authenticated))

            dados_autenticacao: PayloadJWT = PayloadJWT(usuario.id_uuid, tempo_expiracao)

            token: str = UtilsJWT.encode(dados_autenticacao.__dict__, server.http.application.secret_key)

            return ResponseSuccess(data=f"Bearer {token}")