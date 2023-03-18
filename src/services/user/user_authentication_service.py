from datetime import datetime, timedelta
from dataclasses import dataclass

from start import app
from patterns.repository import IAuthRepository
from repositories.user import UserAuthRepository, UserAuthRepositoryParam
from server.utils import UtilsJWT, Constants
from utils.entities import PayloadUserJWT
from models import User


@dataclass
class UserAuthenticationServiceProps:
    email: str
    password: str


class UserAuthenticationService:
    def execute(self, props: UserAuthenticationServiceProps) -> str:
        with app.databases.create_session() as session:
            repository: IAuthRepository[
                UserAuthRepositoryParam, User
            ] = UserAuthRepository(session)

            user: User = repository.auth(props)

            max_time: float = Constants.Authentication.max_minute_authenticated

            expired: float = (datetime.now() + timedelta(minutes=max_time)).timestamp()

            payload: PayloadUserJWT = PayloadUserJWT(user.id_uuid, expired)

            token: str = UtilsJWT.encode(payload.__dict__, app.http.configs.secret_key)

            return f"Bearer {token}"
