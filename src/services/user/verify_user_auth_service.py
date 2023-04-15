from dataclasses import dataclass
from datetime import datetime

from server import App
from utils import UtilsJWT
from patterns.service import IService
from models import User
from .user_finding_service import UserFindingService, UserFindingServiceProps
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
    def execute(self, props: VerifyUserAuthServiceProps) -> User:
        if not props.token:
            raise AuthorizationNotFoundHeader()

        if "Bearer" not in props.token:
            raise TokenTypeNotBearerError()

        token = props.token.replace("Bearer ", "")

        payload: PayloadUserJWT = UtilsJWT.decode(
            token, App.http.configs.secret_key, class_=PayloadUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        service: IService[UserFindingServiceProps, User] = UserFindingService()

        service_props: UserFindingServiceProps = UserFindingServiceProps(
            user_uuid=payload.user_uuid
        )

        user: User = service.execute(service_props)

        return user
