from typing import List, Dict, Any
from dataclasses import dataclass

from start import app
from server.websocket import Controller
from middlewares.websocket import UserAuthenticationMiddleware
from models import Usuario


@dataclass
class UserSocket:
    id: str


@app.websocket.add_controller("/user")
class UserController(Controller):
    __users: List[Dict[str, Any]] = []

    @classmethod
    def get_users(cls) -> List[Dict[str, Any]]:
        return cls.__users

    @UserAuthenticationMiddleware.apply()
    def on_connect(self, auth_user: Usuario) -> None:
        socket_id: str = app.websocket.global_request.sid

        UserController.users.append(
            {
                "name": auth_user.nome,
                "email": auth_user.email,
                "document": auth_user.cpf,
                "date": str(auth_user.data_nascimento),
                "uuid": auth_user.id_uuid,
                "session_id": socket_id,
            }
        )

    def on_disconnect(self) -> None:
        socket_id: str = app.websocket.global_request.sid

        for user in UserController.__users:
            if user["session_id"] == socket_id:
                UserController.__users.remove(user)

    def on_receive_message(self, data: Dict[str, Any]) -> None:
        print("USUÁRIO COMUM RECEBEU A SEGUINTE MENSAGEM:  ", data)

    def on_send_message(self, data: Dict[str, Any]) -> None:
        app.websocket.emit_controller("/departament_user", "receive_message", data)
