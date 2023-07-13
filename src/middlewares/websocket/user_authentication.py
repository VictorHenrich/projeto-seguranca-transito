from typing import Mapping

from server.websocket import SocketMiddleware
from patterns.service import IService
from models import User
from services.user import VerifyUserAuthService
from server import SocketServer


class UserAuthenticationMiddleware(SocketMiddleware):
    def handle(self, props: None) -> Mapping[str, User]:
        token: str = SocketServer.global_request.headers.get("Authorization") or ""

        verify_user_auth_service: IService[User] = VerifyUserAuthService(token)

        user: User = verify_user_auth_service.execute()

        return {"auth": user}
