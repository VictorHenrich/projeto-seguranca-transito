from typing import Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import App
from patterns.repository import IAuthRepository
from repositories.user import UserAuthRepository, UserAuthRepositoryParams
from utils import JWTUtils, ConstantsUtils
from utils.entities import PayloadUserJWT
from models import User


@dataclass
class UserAuthenticationProps:
    email: str
    password: str


class UserAuthenticationService:
    def __init__(
        self, 
        email: str, 
        password: str,
        session: Optional[Session] = None
    ) -> None:
        self.__props: UserAuthenticationProps = UserAuthenticationProps(email, password)
        self.__session: Optional[Session] = session

    def __authenticate(self, session: Session) -> str:
        repository: IAuthRepository[
            UserAuthRepositoryParams, User
        ] = UserAuthRepository(session)

        user: User = repository.auth(self.__props)

        max_time: float = ConstantsUtils.Authentication.max_minute_authenticated

        expired: float = (datetime.now() + timedelta(minutes=max_time)).timestamp()

        payload: PayloadUserJWT = PayloadUserJWT(user.id_uuid, expired)

        token: str = JWTUtils.encode(payload.__dict__, App.http.configs.secret_key)

        return f"Bearer {token}"


    def execute(self) -> str:
        if self.__session:
            return self.__authenticate(self.__session)

        with App.databases.create_session() as session:
            return self.__authenticate(session)
