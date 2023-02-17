from start import app
from server.websocket import Controller


@app.websocket.add_controller("user_connect")
class UserConnectController(Controller):
    def on_connect_server(self, data) -> None:
        print("AAAAAAAAAAAAAAAAAAAAA", data)
