from typing import Dict, TypeAlias, Any

from start import app
from server.websocket import Controller, ConnectionController
from middlewares.websocket import DepartamentUserAuthenticationMiddleware


JSONType: TypeAlias = Dict[str, Any]


class ConnectionDepartamentUser(ConnectionController):
    def __init__(self, id: str, name: str) -> None:
        self.name = name

        super().__init__(id)


@app.websocket.add_controller("/departament_user")
class DepartamentUserController(Controller[ConnectionDepartamentUser]):

    # @DepartamentUserAuthenticationMiddleware.apply()
    def on_open(self, connection: ConnectionController) -> ConnectionDepartamentUser:
        connection_departament_user: ConnectionDepartamentUser = (
            ConnectionDepartamentUser(connection.id, "TESTE")
        )

        return connection_departament_user

    def on_send_message_user(self, data: JSONType):
        pass

    def on_send_message_departament_user(self, data: JSONType):
        pass
