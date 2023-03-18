from datetime import datetime, timedelta

from start import app
from server.database import Database
from patterns.repository import IAuthRepository
from repositories.user import UserAuthRepository, UserAuthRepositoryParam
from server.utils import UtilsJWT, Constants
from utils.entities import PayloadUserJWT
from models import User


class UserAuthenticationService:
    def __handle_repository_param(
        self, email: str, password: str
    ) -> UserAuthRepositoryParam:
        return UserAuthRepositoryParam(email=email.upper(), password=password)

    def execute(self, email: str, password: str) -> str:
        with app.databases.create_session() as session:
            repository: IAuthRepository[
                UserAuthRepositoryParam, User
            ] = UserAuthRepository(session)

            repository_param: UserAuthRepositoryParam = self.__handle_repository_param(
                email, password
            )

            user: User = repository.auth(repository_param)

            max_time: float = Constants.Authentication.max_minute_authenticated

            expired: float = (datetime.now() + timedelta(minutes=max_time)).timestamp()

            payload: PayloadUserJWT = PayloadUserJWT(user.id_uuid, expired)

            token: str = UtilsJWT.encode(payload.__dict__, app.http.configs.secret_key)

            return f"Bearer {token}"
