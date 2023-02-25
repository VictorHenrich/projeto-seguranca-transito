from typing import List, Dict, Any

from start import app
from server.websocket import Controller


@app.websocket.add_controller('/user')
class UserController(Controller):
    __users: List[str] = []

    def on_connect(self) -> None:
        socket_id: str = app.websocket.global_request.sid

        UserController.__users.append(socket_id)
    

    def on_disconnect(self) -> None:
        socket_id: str = app.websocket.global_request.sid

        UserController.__users.remove(socket_id)

    
    def on_receive_message(self, data: Dict[str, Any]) -> None:
        print('USUÁRIO COMUM RECEBEU A SEGUINTE MENSAGEM:  ', data)

    def on_send_message(self, data: Dict[str, Any]) -> None:
        app.websocket.emit_controller("/departament_user", "receive_message", data)
