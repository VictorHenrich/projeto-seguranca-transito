from typing import Dict, TypeAlias, Any, List

from start import app
from server.websocket import Controller, ConnectionController
from middlewares.websocket import DepartamentUserAuthenticationMiddleware
from .user_controller import ConnectionUser


JSONType: TypeAlias = Dict[str, Any]


class ConnectionDepartamentUser(ConnectionController):
    def __init__(self, id: str, name: str, email: str) -> None:
        self.name = name
        self.email = email

        super().__init__(id)


@app.websocket.add_controller("/departament_user")
class DepartamentUserController(Controller[ConnectionDepartamentUser]):

    # @DepartamentUserAuthenticationMiddleware.apply()
    def on_open(self, connection: ConnectionController) -> ConnectionDepartamentUser:
        connection_departament_user: ConnectionDepartamentUser = (
            ConnectionDepartamentUser(connection.id, "Victor Henrich", "victorhenrich993@gmail.com")
        )

        return connection_departament_user

    def on_send_message_user(self, data: JSONType) -> None:
        pass

    def on_send_message_departament_user(self, data: JSONType) -> None:
        departament_user_uuid: str = data['departament_user_uuid']

        message: str = data['body']

    def on_get_users(self, data: JSONType) -> None:
        socket_id: str = app.websocket.global_request.sid

        user_controller: Controller[ConnectionUser] = app.websocket.get_controller('/user')

        users: List[JSONType] = [
            {
                "nome": "Victor Henrich",
                "email": "victorhenrich993@gmail.com",
                "id": user.id
            }
            for user in user_controller.connections
        ]

        self.emit('get_users', users, room=socket_id)

    def on_get_departament_users(self, data: JSONType) -> None:
        socket_id: str = app.websocket.global_request.sid

        departament_users: List[JSONType] = [
            {
                "nome": user.name,
                "email": user.email,
                "id": user.id
            }
            for user in self.connections
        ]

        self.emit('get_departament_users', departament_users, room=socket_id)
