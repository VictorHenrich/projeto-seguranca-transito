from typing import Dict

from server.websocket import SocketMiddleware
from patterns.service import IService
from models import User
from services.user import VerifyUserAuthService, VerifyUserAuthServiceProps
from server import App


class UserAuthenticationMiddleware(SocketMiddleware[None]):
    def handle(self, props: None) -> Dict[str, User]:
        token: str = App.websocket.global_request.headers.get("Authorization") or ""

        verify_user_auth_props: VerifyUserAuthServiceProps = VerifyUserAuthServiceProps(
            token
        )

        verify_user_auth_service: IService[
            VerifyUserAuthServiceProps, User
        ] = VerifyUserAuthService()

        user = verify_user_auth_service.execute(verify_user_auth_props)

        return {"auth": user}
