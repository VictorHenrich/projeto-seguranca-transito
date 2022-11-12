from flask import request
from typing import Optional
from datetime import datetime

from services.http import Middleware
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





class UserAuthentication(Middleware):
    @classmethod
    def handle(cls):
        token: Optional[str] = request.headers.get('Authorization')

        if not token:
            raise AuthorizationNotFoundHeader()

        if 'BEARER' not in token.upper():
            raise TokenTypeNotBearerError()

        payload: PayloadJWT = \
            UtilsJWT.decode(token, server.http.configs.secret_key, PayloadJWT)

        if payload.expired >= datetime.now().timestamp():
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

        