from flask import request
from typing import Optional
from datetime import datetime

from services.http import Middleware, ResponseInauthorized
from services.database import Database
from services.utils import UtilsJWT
from models import Usuario
from exceptions import (
    AuthorizationNotFoundHeader, 
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError
)
from patterns.autenticacao import PayloadJWT
from start import server



db: Database = server.databases.get_database()





class UserAuthenticationMiddleware(Middleware):
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

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        with db.create_session() as session:
            usuario: Optional[Usuario] = \
                session\
                    .query(Usuario)\
                    .filter(Usuario.id_uuid == payload.uuid_user)\
                    .first()

            if not usuario:
                raise UserNotFoundError()

            return {"auth": usuario}

    @classmethod
    def catch(cls, exception: Exception):
        exceptions: list[Exception] = [
            ExpiredTokenError,
            UserNotFoundError,
            TokenTypeNotBearerError
        ]

        if type(exception) in exceptions:
            return ResponseInauthorized(data=str(exception))

        raise exception
        