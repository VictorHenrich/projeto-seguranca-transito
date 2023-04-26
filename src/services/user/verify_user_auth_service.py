from dataclasses import dataclass
from datetime import datetime

from server import App
from utils import UtilsJWT
from patterns.service import IService
from models import User
from .user_finding_service import UserFindingService
from exceptions import (
    AuthorizationNotFoundHeader,
    TokenTypeNotBearerError,
    ExpiredTokenError,
)
from utils.entities import PayloadUserJWT


@dataclass
class VerifyUserAuthServiceProps:
    token: str


class VerifyUserAuthService:
    def __init__(self, token: str) -> None:
        self.__props: VerifyUserAuthServiceProps = VerifyUserAuthServiceProps(token)

    def execute(self) -> User:
        if not self.__props.token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in self.__props.token:
            raise TokenTypeNotBearerError()

        token = self.__props.token.replace("Bearer ", "")

        payload: PayloadUserJWT = UtilsJWT.decode(
            token, App.http.configs.secret_key, class_=PayloadUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        service: IService[User] = UserFindingService(user_uuid=payload.user_uuid)

        user: User = service.execute()

        return user
