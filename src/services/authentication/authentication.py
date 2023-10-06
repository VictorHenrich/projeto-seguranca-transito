from typing import Optional
from datetime import datetime, timedelta

from server import Databases, HttpServer
from patterns.repository import IAuthRepository
from repositories.user import UserAuthRepository, UserAuthRepositoryParams
from utils import JWTUtils, ConstantsUtils
from utils.entities import PayloadUserJWT, UserAuthPayload
from models import User


class AuthenticationService:
    def __init__(
        self, credentials: Optional[UserAuthPayload] = None, user: Optional[User] = None
    ) -> None:
        self.__credentials: Optional[UserAuthPayload] = credentials
        self.__user: Optional[User] = user

    def __find_user(self) -> User:
        if not self.__credentials:
            raise Exception(
                "Nenhuma credencial foi definida para executar a ação de busca!"
            )

        with Databases.create_session() as session:
            repository: IAuthRepository[
                UserAuthRepositoryParams, User
            ] = UserAuthRepository(session)

            return repository.auth(self.__credentials)

    def __get_user(self) -> User:
        if self.__credentials:
            return self.__find_user()

        elif self.__user:
            return self.__user

        else:
            raise Exception("Nenhum tipo de busca foi definido!")

    def execute(self) -> str:
        user: User = self.__get_user()

        max_time: float = ConstantsUtils.Authentication.max_minute_authenticated

        expired: float = (datetime.now() + timedelta(minutes=max_time)).timestamp()

        payload: PayloadUserJWT = PayloadUserJWT(user.id_uuid, expired)

        token: str = JWTUtils.encode(payload.__dict__, HttpServer.config.secret_key)

        return f"Bearer {token}"
