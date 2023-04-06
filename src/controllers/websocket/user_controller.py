from server import App
from server.websocket import Controller, ConnectionController


class ConnectionUser(ConnectionController):
    def __init__(self, id: str) -> None:
        super().__init__(id)


@App.websocket.add_controller("/user")
class UserController(Controller[ConnectionUser]):
    def on_open(self, connection: ConnectionController) -> ConnectionUser:
        return ConnectionUser(connection.id)

    def on_send_message(self) -> None:
        pass
