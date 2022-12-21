from datetime import datetime, timedelta

from start import app
from server.database import Database
from patterns.repository import IAuthRepository
from patterns.service import IService
from repositories.user import (
    UserAuthRepository,
    UserAuthRepositoryParam
)
from server.utils import UtilsJWT, Constants
from utils.entities import PayloadUserJWT
from models import Usuario




class UserAuthenticationService:
    def __handle_repository_param(
        self,
        email: str,
        password: str
    ) -> UserAuthRepositoryParam:
        return UserAuthRepositoryParam(
            email,
            password
        )

    def execute(
        self,
        email: str,
        password: str
    ) -> str:
        database: Database = app.databases.get_database()

        repository: IAuthRepository[UserAuthRepositoryParam, Usuario] = UserAuthRepository(database)

        repository_param: UserAuthRepositoryParam = \
            self.__handle_repository_param(
                email,
                password
            )

        user: Usuario = repository.auth(repository_param)

        max_time: float = Constants.Authentication.max_minute_authenticated
        
        expired: float = (datetime.now() + timedelta(minutes=max_time)).timestamp()

        payload: PayloadUserJWT = PayloadUserJWT(user.id_uuid, expired)

        token: str = UtilsJWT.encode(payload.__dict__, app.http.configs.secret_key)

        return f"Bearer {token}"