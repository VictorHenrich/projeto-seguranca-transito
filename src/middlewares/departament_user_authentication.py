from flask import request
from typing import Optional
from datetime import datetime

from services.http import Middleware, ResponseInauthorized
from services.database import Database
from services.utils import UtilsJWT
from models import UsuarioDepartamento, Departamento
from exceptions import (
    AuthorizationNotFoundHeader, 
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError,
    DepartamentNotFoundError
)
from patterns.autenticacao import PayloadJWT
from start import server



db: Database = server.databases.get_database()





class DepartamentUserAuthenticationMiddleware(Middleware):
    @classmethod
    def handle(cls):
        token: Optional[str] = request.headers.get('Authorization')

        if not token:
            raise AuthorizationNotFoundHeader()

        if 'Bearer' not in token:
            raise TokenTypeNotBearerError()

        token = token.replace('Bearer ', '')

        payload: PayloadJWT = \
            UtilsJWT.decode(token, server.http.configs.secret_key, PayloadJWT)

        if payload.expired >= datetime.now().timestamp():
            raise ExpiredTokenError()

        with db.create_session() as session:
            usuario: Optional[UsuarioDepartamento] = \
                session\
                    .query(UsuarioDepartamento)\
                    .filter(UsuarioDepartamento.id_uuid == payload.uuid_user)\
                    .first()

            if not usuario:
                raise UserNotFoundError()

            departamento: Optional[Departamento] = \
                session\
                    .query(Departamento)\
                    .filter(
                        Departamento.id == usuario.id_departamento
                    )\
                    .first()

            if not departamento:
                raise DepartamentNotFoundError()

            return {"auth_user": usuario, "auth_departament": departamento}


    @classmethod
    def catch(cls, exception: Exception):
        if type(exception) is DepartamentNotFoundError or type(exception) is UserNotFoundError:
            return ResponseInauthorized(data=str(exception))

        raise exception


        