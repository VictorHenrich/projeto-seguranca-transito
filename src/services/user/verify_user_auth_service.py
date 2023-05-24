from dataclasses import dataclass
from datetime import datetime

from server import App
from utils.jwt import JWTUtils
from utils import JWTUtils
from utils.entities import PayloadUserJWT
from patterns.repository import IFindRepository
from models import User
from repositories.user import UserFindRepository, UserFindRepositoryParams
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
)


@dataclass
class VerifyUserAuthProps:
    token: str


@dataclass
class FindUserProps:
    user_uuid: str


class VerifyUserAuthService:
    def __init__(self, token: str) -> None:
        self.__props: VerifyUserAuthProps = VerifyUserAuthProps(token)

    def execute(self) -> User:
        if not self.__props.token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in self.__props.token:
            raise TokenTypeNotBearerError()

        token = self.__props.token.replace("Bearer ", "")

        payload: PayloadUserJWT = JWTUtils.decode(
            token, App.http.configs.secret_key, class_=PayloadUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        with App.databases.create_session() as session:
            user_find: IFindRepository[
                UserFindRepositoryParams, User
            ] = UserFindRepository(session)

            user: User = user_find.find_one(FindUserProps(payload.user_uuid))

            return user
