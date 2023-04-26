from datetime import datetime, timedelta
from dataclasses import dataclass

from server import App
from patterns.repository import IAuthRepository
from repositories.user import UserAuthRepository, UserAuthRepositoryParams
from utils import JWTUtils, ConstantsUtils
from utils.entities import PayloadUserJWT
from models import User


@dataclass
class UserAuthenticationServiceProps:
    email: str
    password: str


class UserAuthenticationService:
    def __init__(self, email: str, password: str) -> None:
        self.__props: UserAuthenticationServiceProps = UserAuthenticationServiceProps(
            email, password
        )

    def execute(self) -> str:
        with App.databases.create_session() as session:
            repository: IAuthRepository[
                UserAuthRepositoryParams, User
            ] = UserAuthRepository(session)

            user: User = repository.auth(self.__props)

            max_time: float = ConstantsUtils.Authentication.max_minute_authenticated

            expired: float = (datetime.now() + timedelta(minutes=max_time)).timestamp()

            payload: PayloadUserJWT = PayloadUserJWT(user.id_uuid, expired)

            token: str = JWTUtils.encode(payload.__dict__, App.http.configs.secret_key)

            return f"Bearer {token}"
